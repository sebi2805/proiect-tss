# just to make sure i want to delete the cache
 rm -rf .mutmut-cache
 rm -rf mutants

PYTHONPATH=. mutmut run
PYTHONPATH=. mutmut results
PYTHONPATH=. mutmut html
mutmut results