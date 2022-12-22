@set pythonpath=src
python tests\helperTests.py 2>test.log 
python tests\commandTests.py 2>>test.log 
python tests\parserTests.py 2>>test.log  
	python tests\runTimeTests.py 2>>test.log  
python tests\expressionTests.py 2>>test.log   
python tests\functionTests.py 2>>test.log   
