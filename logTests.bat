@set pythonpath=src
python tests\helperTests.py 2>test.log 
python tests\commandTests.py 2>>test.log 
python tests\parserTests.py 2>>test.log  
	python tests\editorTests.py 2>>test.log  
python tests\expressionTests.py 2>>test.log   
python tests\functionTests.py 2>>test.log   
python tests\matrixTests.py 2>>test.log   
	python tests\readWriteTests.py 2>>test.log  
python tests\runtimeTests.py 2>>test.log   

