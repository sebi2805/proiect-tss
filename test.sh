# run all the tests, one per line
pytest test/test_boundary.py
pytest test/test_decision_coverage.py
pytest test/test_equivalence_partitioning.py
pytest test/test_independent_circuits.py
pytest test/test_mutation.py
pytest test/test_user_manager_coditional.py


pytest --cov=src --cov-report=term-missing test/test_boundary.py
pytest --cov=src --cov-report=term-missing test/test_decision_coverage.py
pytest --cov=src --cov-report=term-missing test/test_equivalence_partitioning.py
pytest --cov=src --cov-report=term-missing test/test_independent_circuits.py
pytest --cov=src --cov-report=term-missing test/test_mutation.py
pytest --cov=src --cov-report=term-missing test/test_user_manager_coditional.py
