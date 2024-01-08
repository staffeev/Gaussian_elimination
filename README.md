## Программа для решения СЛАУ методом Гаусса

Этот репозиторий предназначен для раззработки программы для решения систем линейных алгебраических уравнений методом Гаусса. 

В [`solver.py`](https://github.com/staffeev/Gaussian_elimination/blob/main/solver.py) файле содержится сама реализация алгоритма Гаусса. В [`solver_with_prints.py`](https://github.com/staffeev/Gaussian_elimination/blob/main/solver_with_prints.py) файле содержится тот же самый алгоритм, но с большим количеством промежуточных выводов (т.е. решением)

В файле [`main.py`](https://github.com/staffeev/Gaussian_elimination/blob/main/main.py) содержится код, решающий СЛАУ, введенную пользователем в консоль. В других файлах СЛАУ вновится прямо в код.

Исполняемый файл, который выполняет те же функции, то и `main.py`, доступен в релизах (или [здесь](https://github.com/staffeev/Gaussian_elimination/releases/download/v1.0/main.exe))
