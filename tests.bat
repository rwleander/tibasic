@set pythonpath=src
del test*.ti
python tests\helperTests.py 
python tests\commandTests.py 
