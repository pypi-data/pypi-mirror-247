import win32com.client
import pywintypes
import pathlib
from robot.api.deco import keyword, library
import win32com.client
from types import NoneType
import xml.etree.ElementTree as ET
from robot.api import logger


def _create_debug_out_param(paramObject):
    _table_header = """<table border=1><thead><tr><th colspan="3">Teststand parameter object</th>
                       </tr><tr><th>Name</th><th>Value</th></tr></thead><tbody>"""
    _table_footer = """</tbody></table>"""
    xmlres = paramObject.GetXML(0, 0)
    pairs = ((f"{item.attrib['Name']}", f"{[i.text for i in item][0]}",) for item in  ET.fromstring(xmlres))
    return _table_header + "".join(f"""<tr><th>{name}</th><td>{value}</td></tr>""" for name, value in pairs) + _table_footer


def _make_execution_log_from_xml(res):
    def _traverse(element, level=0):
        try:
            nameVal = element.attrib["Name"]
            if nameVal in {"Sequence","SequenceFile", "StepName"}:
                color = {"Sequence": "purple", "SequenceFile": "navy", "StepName":"black"}[nameVal]
                yield f"""{"&nbsp;"*((level//5)*4)}<span style="color: {color};">{element[0].text}</span><br>"""
        except:
            pass
        for child in element:
            yield from _traverse(child, level + 1)
    root = ET.fromstring(res)
    return "".join(_traverse(root))


@library(scope='GLOBAL')
class teststand_tamer:
    """This library allows to extend robotframework with teststand

    This is intended to be used in batch mode. Do what needs to be donne and terminate.
    This library does not try to release all objects created.

    - Releasing the parameter object makes its content unreachable.
    - Boxing the parameter objects is overkill.
    - Reusing parameter objects makes this an non issue.
    - Sequence Files are cached. Clearing the cache on exit is wasted effort.

    Please configure teststand to not check for resource leaks. If you do encounter
    issues, consider to move from a alloc/free concept to an alloc/reuse concept.
    """
    _nrOfTeststandTamers = 0
    __tsEngine = None
    execution_timeout = 600000

    @property 
    def process_model_entry_point(self, pmep):
        logger.warning("This funcitonaltiy is highly experimental. So far there was only success with None models!")
        pmep = pathlib.Path(pmep).resolve(strict=True)
        self._process_model_entry_point = self.__tsEngine.GetSequenceFileEx(pmep, 107)

    def __init__(self, tsenv_path=None):
        """
        The path to the env configuration is optional.
        """
        assert self._nrOfTeststandTamers == 0, "There can be only one teststand tamer..."
        teststand_tamer._nrOfTeststandTamers = 1
        if tsenv_path:
            tsenv_path = pathlib.Path(tsenv_path).resolve(strict=True)
            tsEngineInitSettings = win32com.client.Dispatch("{DEF1D36A-327A-487D-876D-816D0D171888}")
            tsEngineInitSettings.SetEnvironmentPath(str(tsenv_path))       
        self.__tsEngine = win32com.client.Dispatch("TestStand.Engine")
        self._process_model_entry_point=None

    @keyword
    def get_teststand_version(self):
        """Get the testand version as a string
        
        This does not include addtional information like 
        64bit/32bit versions.
        """
        return f"{self.__tsEngine.MajorVersion}.{self.__tsEngine.MinorVersion}"

    @keyword
    def run_teststand_sequence(self, sequencefile, sequence, preexisitng_param_object=None, **paramters):
        """Execute a teststand sequence, passing parameters.

        The keyword first creates/modifies the parameter object for the call.
        The datatype is infered from the datatype of the keyword arguments.:
        - Number (float)
        - Integer64 (signed integer number)
        - Interface (Provide None to create an initial Nothing)

        To access the modified value of a by reference parameter, this parameter 
        needs to be created ahead of the call.

        === Logging of teststand execution ===

        The logged execution information from teststand is a visualisation of
        the result object. There is the name of the step, the name of the squence, and the name of
        the sequence file in the log.

        When subsequences are called, the subsequence steps are shown ahead of
        the call step, the success and the paramters are not shown.
        """
        if preexisitng_param_object is None:
            logger.debug("creating new param object...")
            preexisitng_param_object = self.__tsEngine.NewPropertyObject(0, False, "Input", 0)
        else:
            logger.debug(f"reusing param object:<br><br>{_create_debug_out_param(preexisitng_param_object)}", html=True)

        pAdders = {float: preexisitng_param_object.SetValNumber,
                   int:   preexisitng_param_object.SetValInteger64,
                   str:   preexisitng_param_object.SetValString,
                   NoneType:  preexisitng_param_object.SetValInterface}
        
        for pname, pvalue in paramters.items():
            typeOfParam = type(pvalue)
            logger.debug(f"set {pname} to {pvalue}")
            assert typeOfParam in pAdders.keys(), f"unsuported data type: {typeOfParam}."
            pAdders[typeOfParam](pname, 0x1, pvalue)

        sequencefile = pathlib.Path(sequencefile).resolve(strict=True)
        seqFile = self.__tsEngine.GetSequenceFileEx(sequencefile, 107)
        logger.debug(_create_debug_out_param(preexisitng_param_object), html=True)
        execution = self.__tsEngine.NewExecution(seqFile, sequence, self._process_model_entry_point, False, 0, preexisitng_param_object)
        assert execution.WaitForEndEx(float(self.execution_timeout)), "timeout occured!"
        logger.info(f"Sequence {sequence} in {sequencefile} finsihed with status: {execution.ResultStatus}. Teststand might have a liberal understanding on what 'PASS' means...")
        xmlstring = execution.ResultObject.GetXML(0, "1")
        logger.info(_make_execution_log_from_xml(xmlstring), html=True)
        assert execution.ResultStatus == 'Passed'
        execution = None
        return preexisitng_param_object
    
    @staticmethod
    @keyword
    def get_from_teststand_parameter(param_object, key):
        """Returns a value from the given ``parameter object`` based on the given ``key``.

        If the given ``key`` cannot be found from the ``dictionary``, this
        keyword fails.

        This keyword tries to follow the conventions of the Get From Dictionary
        keyword, from the collections library.
        """
        try:
            return param_object.GetValVariant(key, 0)
        except pywintypes.com_error as e:
            logger.error(e)
        raise KeyError(f"{key} is not accessible in this teststand parameter object") 
