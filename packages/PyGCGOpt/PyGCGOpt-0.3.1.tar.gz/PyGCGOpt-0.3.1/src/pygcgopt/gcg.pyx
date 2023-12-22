# distutils: language = c++

from pyscipopt.scip import PY_SCIP_CALL
from pyscipopt.scip cimport Model as SCIPModel
from pyscipopt.scip cimport Variable, Constraint, Solution, SCIP_RESULT, SCIP_DIDNOTRUN, SCIPgetStage, SCIP_STAGE, SCIP_STAGE_PRESOLVED, SCIPvarSetData, SCIPgetBestSol

from cpython cimport Py_INCREF, Py_DECREF

from libc.stdlib cimport malloc, free

from libcpp cimport bool

from typing import List

from pygcgopt.util import str_conversion

from pathlib import Path
import tempfile
import weakref
from copy import copy

from collections.abc import Iterable

include "detector.pxi"
include "pricing_solver.pxi"
include "partition.pxi"
include "decomposition.pxi"
include "detprobdata.pxi"


cdef SCIP_CLOCK* start_new_clock(SCIP* scip):
    cdef SCIP_CLOCK* clock
    PY_SCIP_CALL(SCIPcreateClock(scip, &clock))
    PY_SCIP_CALL(SCIPstartClock(scip, clock))
    return clock


cdef double stop_and_free_clock(SCIP* scip, SCIP_CLOCK* clock):
    PY_SCIP_CALL(SCIPstopClock(scip, clock))
    cdef double detection_time = SCIPgetClockTime(scip, clock)
    PY_SCIP_CALL(SCIPfreeClock(scip, &clock))
    return detection_time


cdef class PY_GCG_PRICINGSTATUS:
    UNKNOWN = GCG_PRICINGSTATUS_UNKNOWN
    NOTAPPLICABLE = GCG_PRICINGSTATUS_NOTAPPLICABLE
    SOLVERLIMIT = GCG_PRICINGSTATUS_SOLVERLIMIT
    OPTIMAL = GCG_PRICINGSTATUS_OPTIMAL
    INFEASIBLE = GCG_PRICINGSTATUS_INFEASIBLE
    UNBOUNDED = GCG_PRICINGSTATUS_UNBOUNDED


cdef class Model(SCIPModel):
    """Main class for interaction with the GCG solver."""

    def includeDefaultPlugins(self):
        """Includes all default plug-ins of GCG into SCIP

        Called automatically during initialization of the model.
        """
        PY_SCIP_CALL(SCIPincludeGcgPlugins(self._scip))

    def addVar(self, *args, **kwargs):
        pyVar = <Variable>super().addVar(*args, **kwargs)

        SCIPvarSetData(pyVar.scip_var, NULL)

        return pyVar

    def presolve(self):
        """Presolve the problem."""
        PY_SCIP_CALL(GCGpresolve(self._scip))

    def detect(self):
        """Detect the problem.

        Can be executed before or after presolving. If executed before presolving, the structure is detected on the original problem and presolving is skiped when solving the problem later.

        .. seealso:: * :meth:`presolve`
                     * :meth:`optimize`
        """
        PY_SCIP_CALL(GCGdetect(self._scip))

    def printStatistics(self):
        """Print solving statistics of GCG to stdout."""
        PY_SCIP_CALL(GCGprintStatistics(self._scip, NULL))

    def printVersion(self):
        """Print version, copyright information and compile mode of GCG and SCIP"""
        GCGprintVersion(self._scip, NULL)

        super().printVersion()

    def optimize(self):
        """Optimize the problem.

        This will transform, presolve and detect the problem if neccessary.
        Otherwise, GCG will solve the problem directly."""
        PY_SCIP_CALL(GCGsolve(self._scip))
        self._bestSol = Solution.create(self._scip, SCIPgetBestSol(self._scip))

    def getDualbound(self):
        """Retrieve the best dual bound.

        This retrieves the same dual bound that GCG reports in the console log. The dual bound is based on the
        objective value of the optimized linear programming relaxation at the current node.

        .. note:: The dual bound at the root node is *not* always equal to the solution of the restricted master problem LP relaxation. This can be due to master cuts or abortion of the pricing loop *before* the restricted master problem is optimal.

        :return: The best dual bound of the current node.
        """
        return GCGgetDualbound(self._scip)

    def listDecompositions(self) -> List[PartialDecomposition]:
        """Lists all finnished decompositions found during the detection loop or provided by the user."""
        cdef int npartialdecs = GCGconshdlrDecompGetNPartialdecs(self._scip)
        cdef int* decids = <int*>malloc(npartialdecs * sizeof(int))

        GCGconshdlrDecompGetFinishedPartialdecsList(self._scip, &decids, &npartialdecs)

        decomps = [PartialDecomposition.create(GCGconshdlrDecompGetPartialdecFromID(self._scip, decids[i])) for i in range(npartialdecs)]

        free(decids)

        return decomps

    def addDecompositionFromConss(self, master_conss, *block_conss):
        """Adds a user specified decomposition to GCG based on constraints.

        :param master_conss: An iterable of Constraint objects. Can be the empty list.
        :param block_conss: Any number of lists. The Constraints from each list will be turned into their own block. (optional)
        :return: The created PartialDecomposition object

        Creates a PartialDecomposition object using createDecomposition(). Fixes the master constraints with
        fixMasterConss() and the block constraints with fixBlockConss(). The decomposition is added with addDecomposition().
        """
        cdef PartialDecomposition pd = self.createDecomposition()
        pd.fixConssToMaster(master_conss)
        for idx, conss in enumerate(block_conss):
            if not isinstance(conss, Iterable):
                pd.fixConsToBlock(conss, idx)
            else:
                pd.fixConssToBlock(conss, idx)
        self.addDecomposition(pd)
        return pd

    def addPreexistingPartialDecomposition(self, PartialDecomposition partialdec):
        self.addDecomposition(partialdec)

    def addDecomposition(self, PartialDecomposition partialdec):
        """Adds a user specified decomposition to GCG.

        The passed PartialDecomposition can be partial or finnished. A partial decomposition will be completed by GCG using
        its detector loop. If a finnished decomposition is passed, GCG will skip the detection loop and use the
        provided decomposition right away.
        """
        partialdec.prepare()
        partialdec.setUsergiven()
        GCGconshdlrDecompAddPreexisitingPartialDec(self._scip, partialdec.thisptr)

    def createPartialDecomposition(self):
        return self.createDecomposition()

    def createDecomposition(self):
        """Creates a new empty PartialDecomposition.

        The created PartialDecomposition object can be used to fix constraints and variables. Afterwards, it can be
        passed to the model through addPreexistingPartialDecomposition().

        .. seealso:: * :meth:`PartialDecomposition.fixConsToMaster`
                     * :meth:`PartialDecomposition.fixConssToMaster`
                     * :meth:`PartialDecomposition.fixConsToBlock`
                     * :meth:`PartialDecomposition.fixConssToBlock`
                     * :meth:`PartialDecomposition.fixConsToBlockId`
                     * :meth:`PartialDecomposition.fixConssToBlockId`
        """
        cdef bool is_presolved = self.getStage() >= SCIP_STAGE_PRESOLVED
        cdef PARTIALDECOMP *decomp = new PARTIALDECOMP(self._scip, not is_presolved)
        return PartialDecomposition.create(decomp)

    def includePricingSolver(self, PricingSolver pricingSolver, solvername, desc, priority=0, heuristicEnabled=False, exactEnabled=False):
        c_solvername = str_conversion(solvername)
        c_desc = str_conversion(desc)

        PY_SCIP_CALL(GCGpricerIncludeSolver(
            (<SCIPModel>self.getMasterProb())._scip, c_solvername, c_desc, priority, heuristicEnabled, exactEnabled, PyPricingSolverUpdate,
            PyPricingSolverSolve, PyPricingSolverSolveHeur, PyPricingSolverFree, PyPricingSolverInit, PyPricingSolverExit,
            PyPricingSolverInitSol, PyPricingSolverExitSol, <GCG_SOLVERDATA*>pricingSolver))

        pricingSolver.model = <SCIPModel>weakref.proxy(self)
        pricingSolver.solvername = solvername
        Py_INCREF(pricingSolver)

    def listPricingSolvers(self):
        cdef SCIPModel mp = <SCIPModel>self.getMasterProb()
        cdef int n_pricing_solvers = GCGpricerGetNSolvers(mp._scip)
        cdef GCG_SOLVER** pricing_solvers = GCGpricerGetSolvers(mp._scip)

        return [GCGsolverGetName(pricing_solvers[i]).decode('utf-8') for i in range(n_pricing_solvers)]

    def setPricingSolverEnabled(self, pricing_solver_name, is_enabled=True):
        """Enables or disables exact and heuristic solving for the specified pricing solver.

        :param pricing_solver_name: The name of the pricing solver.
        :param is_enabled: Decides weather the pricing solver should be enabled or diabled.

        This is a convenience method to access the boolean parameters "pricingsolver/<name>/exactenabled" and
        "pricingsolver/<name>/heurenabled".

        Use :meth:`listPricingSolvers()` to obtain a list of all pricing solvers.
        """
        self.setPricingSolverExactEnabled(pricing_solver_name, is_enabled)
        self.setPricingSolverHeuristicEnabled(pricing_solver_name, is_enabled)

    def setPricingSolverExactEnabled(self, pricing_solver_name, is_enabled=True):
        """Enables or disables exact solving for the specified pricing solver.

        :param pricing_solver_name: The name of the pricing solver.
        :param is_enabled: Decides weather the pricing solver should be enabled or diabled.

        This is a convenience method to access the boolean parameter "pricingsolver/<name>/exactenabled".

        Use :meth:`listPricingSolvers()` to obtain a list of all pricing solvers.
        """
        self.setBoolParam("pricingsolver/{}/exactenabled".format(pricing_solver_name), is_enabled)

    def setPricingSolverHeuristicEnabled(self, pricing_solver_name, is_enabled=True):
        """Enables or disables heuristic solving for the specified pricing solver.

        :param pricing_solver_name: The name of the pricing solver.
        :param is_enabled: Decides weather the pricing solver should be enabled or diabled.

        This is a convenience method to access the boolean parameter "pricingsolver/<name>/heurenabled".

        Use :meth:`listPricingSolvers()` to obtain a list of all pricing solvers.
        """
        self.setBoolParam("pricingsolver/{}/heurenabled".format(pricing_solver_name), is_enabled)

    def includeDetector(self, Detector detector, detectorname, decchar, desc, freqcallround=1, maxcallround=INT_MAX, mincallround=0, freqcallroundoriginal=1, maxcallroundoriginal=INT_MAX, mincallroundoriginal=0, priority=0, enabled=True, enabledfinishing=False, enabledpostprocessing=False, skip=False, usefulrecall=False):
        """includes a detector

        :param detector: An object of a subclass of detector#Detector.
        :param detectorname: name of the detector

        For an explanation for all arguments, see :meth:`DECincludeDetector()`.
        """
        if len(decchar) != 1:
            raise ValueError("Length of value for 'decchar' must be 1")

        c_detectorname = str_conversion(detectorname)
        c_decchar = ord(str_conversion(decchar))
        c_desc = str_conversion(desc)
        PY_SCIP_CALL(DECincludeDetector(
            self._scip, c_detectorname, c_decchar, c_desc, freqcallround, maxcallround, mincallround,
            freqcallroundoriginal, maxcallroundoriginal, mincallroundoriginal, priority, enabled, enabledfinishing,
            enabledpostprocessing, skip, usefulrecall, <DEC_DETECTORDATA*>detector, PyDetectorFree, PyDetectorInit,
            PyDetectorExit, PyDetectorPropagatePartialdec, PyDetectorFinishPartialdec, PyDetectorPostprocessPartialdec,
            PyDetectorSetParamAggressive, PyDetectorSetParamDefault, PyDetectorSetParamFast))

        detector.model = <SCIPModel>weakref.proxy(self)
        detector.detectorname = detectorname
        Py_INCREF(detector)

    def listDetectors(self):
        """Lists all detectors that are currently included

        :return: A list of strings of the detector names

        .. note:: The detectors can be enabled or disabled using the appropriate methods by passing the name.

        .. seealso:: * :meth:`setDetectorEnabled`
                     * :meth:`setDetectorFinishingEnabled`
                     * :meth:`setDetectorPostprocessingEnabled`
        """
        cdef int n_detectors = GCGconshdlrDecompGetNDetectors(self._scip)
        cdef DEC_DETECTOR** detectors = GCGconshdlrDecompGetDetectors(self._scip)

        return [DECdetectorGetName(detectors[i]).decode('utf-8') for i in range(n_detectors)]

    def setDetectorEnabled(self, detector_name, is_enabled=True):
        """Enables or disables a detector for detecting partial decompositions.

        :param detector_name: The name of the detector.
        :param is_enabled: Decides weather the detector should be enabled or diabled.

        This is a convenience method to access the boolean parameter "detection/detectors/<name>/enabled".

        .. note:: Disabling a detector using this method is not enough to ensure that it will not run. In addition setDetectorFinishingEnabled() and setDetectorPostProcessingEnabled() have to be used.

        Use listDetectors() to obtain a list of all detectors.
        """
        # TODO test if detector_name exists
        self.setBoolParam("detection/detectors/{}/enabled".format(detector_name), is_enabled)

    def setDetectorFinishingEnabled(self, detector_name, is_enabled=True):
        """Enables or disables a detector for finishing partial decompositions.

        :param detector_name: The name of the detector.
        :param is_enabled: Decides weather the detector should be enabled or diabled.

        This is a convenience method to access the boolean parameter "detection/detectors/<name>/finishingenabled".

        .. seealso:: * :meth:`setDetectorEnabled`
        """
        # TODO test if detector_name exists
        self.setBoolParam("detection/detectors/{}/finishingenabled".format(detector_name), is_enabled)

    def setDetectorPostprocessingEnabled(self, detector_name, is_enabled=True):
        """Enables or disables a detector for postprocessing partial decompositions.

        :param detector_name: The name of the detector.
        :param is_enabled: Decides weather the detector should be enabled or diabled.

        This is a convenience method to access the boolean parameter "detection/detectors/<name>/postprocessingenabled".

        .. seealso:: * :meth:`setDetectorEnabled`
        """
        # TODO test if detector_name exists
        self.setBoolParam("detection/detectors/{}/postprocessingenabled".format(detector_name), is_enabled)

    def getMasterProb(self):
        """Provides access to the GCG master problem.

        :return: An instance of scip#Model that represents the master problem.
        """
        cdef SCIP * master_prob = GCGgetMasterprob(self._scip)
        return GCGMasterModel.create(master_prob)

    def setGCGSeparating(self, setting):
        """Sets parameter settings of all separators

        :param setting: the parameter settings (SCIP_PARAMSETTING)
        """
        # GCG API is inconsistant with SCIP, SCIPsetSeparating
        PY_SCIP_CALL(GCGsetSeparators(self._scip, setting))

    def writeAllDecomps(self, directory="alldecompositions/", extension="dec", bool original=True, bool presolved=True, createDirectory=True):
        """Writes all decompositions to disk

        :param directory: A path to a folder where to store the decomposition files
        :param extension: Extension without a dot. Decides the output format. Use "dec" to output decomposition files
        :param createDirectory: Automatically create the directory specified in ``directory`` if it does not exist
        """
        if createDirectory:
            Path(directory).mkdir(exist_ok=True, parents=True)
        c_directory = str_conversion(directory)
        c_extension = str_conversion(extension)
        PY_SCIP_CALL(DECwriteAllDecomps(self._scip, c_directory, c_extension, original, presolved))

    def getMastervars(self, var):
        """Returns the master variables corresponding to the variable of original problem

        :param var: Variable of original problem
        :return: List of master variables
        """
        cdef int n_vars = GCGoriginalVarGetNMastervars((<Variable>var).scip_var)
        cdef SCIP_VAR** mastervars = GCGoriginalVarGetMastervars((<Variable>var).scip_var)
        return [Variable.create(mastervars[i]) for i in range(n_vars)]


cdef class GCGPricingModel(SCIPModel):
    @staticmethod
    cdef create(SCIP* scip):
        """Creates a pricing problem model and appropriately assigns the scip and bestsol parameters
        """
        if scip == NULL:
            raise Warning("cannot create Model with SCIP* == NULL")
        model = GCGPricingModel(createscip=False)
        model._scip = scip
        model._bestSol = Solution.create(scip, SCIPgetBestSol(scip))
        return model

    def createGcgCol(self, probnr, variables, vals, bool isray, redcost):
        """create a gcg column

        :param prob: number of corresponding pricing problem
        :param variables: (sorted) array of variables of corresponding pricing problem
        :param vals: array of solution values (belonging to vars)
        :param isray: is the column a ray?
        :param redcost: last known reduced cost
        """
        cdef GCG_COL * gcg_col
        nvars = len(variables)
        cdef SCIP_VAR ** c_vars = <SCIP_VAR**>malloc(nvars * sizeof(SCIP_VAR*))
        cdef SCIP_Real * c_vals = <SCIP_Real*>malloc(nvars * sizeof(SCIP_Real))

        for i in range(nvars):
            c_vars[i] = (<Variable>variables[i]).scip_var
            c_vals[i] = vals[i]

        GCGcreateGcgCol(self._scip, &gcg_col, probnr, c_vars, c_vals, nvars, isray, redcost)

        pyGCGCol = GCGColumn.create(gcg_col)

        free(c_vars)
        free(c_vals)

        return pyGCGCol


cdef class GCGMasterModel(SCIPModel):
    @staticmethod
    cdef create(SCIP* scip):
        """Creates a pricing problem model and appropriately assigns the scip and bestsol parameters
        """
        if scip == NULL:
            raise Warning("cannot create Model with SCIP* == NULL")
        model = GCGMasterModel(createscip=False)
        model._scip = scip
        model._bestSol = Solution.create(scip, SCIPgetBestSol(scip))
        return model

    def addCol(self, GCGColumn col):
        PY_SCIP_CALL(GCGpricerAddCol(self._scip, col.gcg_col))

    def getOrigvars(self, var):
        """Returns the original variables corresponding to the variable of master problem

        :param var: Variable of master problem
        :return: List of original variables
        """
        cdef int n_vars = GCGmasterVarGetNOrigvars((<Variable>var).scip_var)
        cdef SCIP_VAR** originalvars = GCGmasterVarGetOrigvars((<Variable>var).scip_var)
        return [Variable.create(originalvars[i]) for i in range(n_vars)]


cdef class GCGColumn:
    """Base class holding a pointer to corresponding GCG_COL"""

    @staticmethod
    cdef create(GCG_COL* gcgcol):
        if gcgcol == NULL:
            raise Warning("cannot create Column with GCG_COL* == NULL")
        col = GCGColumn()
        col.gcg_col = gcgcol
        return col

    def __hash__(self):
        return hash(<size_t>self.gcg_col)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.gcg_col == (<GCGColumn>other).gcg_col)
