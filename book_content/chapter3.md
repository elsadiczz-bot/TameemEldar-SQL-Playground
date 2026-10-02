# الفصل 3: التجميع

## 3.1 Aggregations — الدوال التجميعية

### الدوال
| الدالة | المعنى |
|--------|--------|
| COUNT() | عد |
| SUM() | مجموع |
| AVG() | متوسط |
| MIN() | أصغر |
| MAX() | أكبر |

### مثال: عدد المرضى

**الاستعلام:**
SELECT COUNT(*) as total FROM patients;

**النتيجة:**
| total |
|-------|
| 20 |

### مثال: متوسط الأعمار

**الاستعلام:**
SELECT ROUND(AVG(age), 1) as avg_age FROM patients;

**النتيجة:**
| avg_age |
|---------|
| 48.4 |

## 3.2 GROUP BY — التجميع

### التعريف
GROUP BY يجمع الصفوف المتشابهة.

### مثال: عدد لكل تشخيص

**الاستعلام:**
SELECT diagnosis, COUNT(*) as count FROM patients GROUP BY diagnosis;

**النتيجة:**
| diagnosis | count |
|-----------|-------|
| Diabetes | 4 |
| Hypertension | 4 |
| Asthma | 4 |
| Stroke | 4 |
| Cancer | 4 |

**ما يفعله:** يقسّم المرضى حسب التشخيص — ويعدّ كل مجموعة.

## 3.3 HAVING — فلترة المجموعات

### الفرق بين WHERE و HAVING
| WHERE | HAVING |
|-------|--------|
| قبل التجميع | بعد التجميع |
| لا يستخدم Aggregations | يستخدم Aggregations |

### مثال

**الاستعلام:**
SELECT diagnosis, COUNT(*) as count 
FROM patients 
GROUP BY diagnosis 
HAVING COUNT(*) > 3;

**النتيجة:**
| diagnosis | count |
|-----------|-------|
| Diabetes | 4 |
| Hypertension | 4 |
| Asthma | 4 |
| Stroke | 4 |
| Cancer | 4 |
