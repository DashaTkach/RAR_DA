import numpy as np
import scipy.stats as sts
from openpyxl import load_workbook
from statsmodels.stats.api import lilliefors

# здесь мы загружаем данные из экселя и формируем список
wb = load_workbook('tables_for_rar.xlsx')
sheet = wb.get_sheet_by_name('Sheet 3')
data = sheet.values
data = list(data)
result = []
for i in data:
    result.append(i[0])
result.pop(0)

# задание 6
# Для математического ожидания
def mean_confidence_interval(x, gamma=0.95):
    x = np.asarray(x)
    n = len(x)
    a, s = np.mean(x), sts.sem(x)
    h = s * sts.t.ppf((1 + gamma) / 2, n - 1)
    return a - h, a + h


print(mean_confidence_interval(result))


#  Ответ: (-0.004505114400426785, 0.006307997664774445)

# Для дисперсии
def var_confidence_interval(x, gamma=0.95):
    x = np.asarray(x)
    n = len(x)
    chi_1 = sts.chi2(df=n - 1).ppf((1 + gamma) / 2)
    chi_2 = sts.chi2(df=n - 1).ppf((1 - gamma) / 2)
    var = np.var(x, ddof=1)
    b1 = (n - 1) * var / chi_1
    b2 = (n - 1) * var / chi_2
    return b1, b2


print(var_confidence_interval(result))


#  Ответ: (0.0026811841618958466, 0.003533890291229843)

# задание 7 - проверка нипотезы
def student_test(x, m_0, alternative='two-sided'):
    if alternative not in ('two-sided', 'less', 'greater'):
        raise ValueError("Альтернатива длжна быть одной из:\'two-sided', 'less' или 'greater'")
    x = np.asarray(x)
    n = float(len(x))
    m = x.mean()
    s = x.std() * (n / (n - 1)) ** 0.5
    t = (m - m_0) * np.sqrt(n) / s
    if alternative == 'two-sided':
        return t, 2 * (1 - sts.t.cdf(np.abs(t), n - 1))
    if alternative == 'less':
        return t, sts.t.cdf(t, n - 1)
    if alternative == 'greater':
        return t, 1 - sts.t.cdf(t, n - 1)


print(student_test(result, 0))
#  Ответ: (0.32776909626656675, 0.7432560439256872)

# задание 10 - уровень значимости гипотезы о нормальном законе распределения
k, p = lilliefors(result)
print('k: %.3f p-value: %.3f' % (k, p))
#  Ответ: k: 0.109 p-value: 0.001
