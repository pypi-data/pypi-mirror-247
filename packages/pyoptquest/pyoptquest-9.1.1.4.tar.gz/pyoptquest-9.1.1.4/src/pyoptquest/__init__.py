from .pyoptquest import OptQuestOptimizer

COptQuestOptimizationEvaluator = None
COptQuestBinaryVariable = None
COptQuestConstraint = None
COptQuestContinuousVariable = None
COptQuestDesignVariable = None
COptQuestDiscreteVariable = None
COptQuestEnumerationVariable = None
COptQuestEquationSolver = None
COptQuestException = None
COptQuestExceptionLogger = None
COptQuestFrontierMultiObjective = None
COptQuestIntegerVariable = None
COptQuestMultiObjective = None
COptQuestObjective = None
COptQuestOptimization = None
COptQuestPermutationGroup = None
COptQuestPermutationVariable = None
COptQuestSingleObjective = None
COptQuestSolution = None
COptQuestStringConstraint = None
COptQuestStringObjective = None
COptQuestUserControlledObjective = None
COptQuestUserControlledVariable = None
COptQuestVariable = None
COptQuestSearchParameters = None


def InitializeOptQuest(path):
  global COptQuestOptimizationEvaluator
  global COptQuestBinaryVariable
  global COptQuestConstraint
  global COptQuestContinuousVariable
  global COptQuestDesignVariable
  global COptQuestDiscreteVariable
  global COptQuestEnumerationVariable
  global COptQuestEquationSolver
  global COptQuestException
  global COptQuestExceptionLogger
  global COptQuestFrontierMultiObjective
  global COptQuestIntegerVariable
  global COptQuestMultiObjective
  global COptQuestObjective
  global COptQuestOptimization
  global COptQuestPermutationGroup
  global COptQuestPermutationVariable
  global COptQuestSingleObjective
  global COptQuestSolution
  global COptQuestStringConstraint
  global COptQuestStringObjective
  global COptQuestUserControlledObjective
  global COptQuestUserControlledVariable
  global COptQuestVariable
  global COptQuestSearchParameters
  from .pyoptquest import InitializeOptQuest
  from .pyoptquest import COptQuestOptimizationEvaluator
  from .pyoptquest import COptQuestBinaryVariable
  from .pyoptquest import COptQuestConstraint
  from .pyoptquest import COptQuestContinuousVariable
  from .pyoptquest import COptQuestDesignVariable
  from .pyoptquest import COptQuestDiscreteVariable
  from .pyoptquest import COptQuestEnumerationVariable
  from .pyoptquest import COptQuestEquationSolver
  from .pyoptquest import COptQuestException
  from .pyoptquest import COptQuestExceptionLogger
  from .pyoptquest import COptQuestFrontierMultiObjective
  from .pyoptquest import COptQuestIntegerVariable
  from .pyoptquest import COptQuestMultiObjective
  from .pyoptquest import COptQuestObjective
  from .pyoptquest import COptQuestOptimization
  from .pyoptquest import COptQuestPermutationGroup
  from .pyoptquest import COptQuestPermutationVariable
  from .pyoptquest import COptQuestSingleObjective
  from .pyoptquest import COptQuestSolution
  from .pyoptquest import COptQuestStringConstraint
  from .pyoptquest import COptQuestStringObjective
  from .pyoptquest import COptQuestUserControlledObjective
  from .pyoptquest import COptQuestUserControlledVariable
  from .pyoptquest import COptQuestVariable
  from .pyoptquest import COptQuestSearchParameters
  pyoptquest.InitializeOptQuest(path)
  COptQuestOptimizationEvaluator = pyoptquest.COptQuestOptimizationEvaluator
  COptQuestBinaryVariable = pyoptquest.COptQuestBinaryVariable
  COptQuestConstraint = pyoptquest.COptQuestConstraint
  COptQuestContinuousVariable = pyoptquest.COptQuestContinuousVariable
  COptQuestDesignVariable = pyoptquest.COptQuestDesignVariable
  COptQuestDiscreteVariable = pyoptquest.COptQuestDiscreteVariable
  COptQuestEnumerationVariable = pyoptquest.COptQuestEnumerationVariable
  COptQuestEquationSolver = pyoptquest.COptQuestEquationSolver
  COptQuestException = pyoptquest.COptQuestException
  COptQuestExceptionLogger = pyoptquest.COptQuestExceptionLogger
  COptQuestFrontierMultiObjective = pyoptquest.COptQuestFrontierMultiObjective
  COptQuestIntegerVariable = pyoptquest.COptQuestIntegerVariable
  COptQuestMultiObjective = pyoptquest.COptQuestMultiObjective
  COptQuestObjective = pyoptquest.COptQuestObjective
  COptQuestOptimization = pyoptquest.COptQuestOptimization
  COptQuestPermutationGroup = pyoptquest.COptQuestPermutationGroup
  COptQuestPermutationVariable = pyoptquest.COptQuestPermutationVariable
  COptQuestSingleObjective = pyoptquest.COptQuestSingleObjective
  COptQuestSolution = pyoptquest.COptQuestSolution
  COptQuestStringConstraint = pyoptquest.COptQuestStringConstraint
  COptQuestStringObjective = pyoptquest.COptQuestStringObjective
  COptQuestUserControlledObjective = pyoptquest.COptQuestUserControlledObjective
  COptQuestUserControlledVariable = pyoptquest.COptQuestUserControlledVariable
  COptQuestVariable = pyoptquest.COptQuestVariable
  COptQuestSearchParameters = pyoptquest.COptQuestSearchParameters
