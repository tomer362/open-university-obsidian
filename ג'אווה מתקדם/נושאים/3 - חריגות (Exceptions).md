# יצירת סוג חדש של חריגה
![[Pasted image 20240715010214.png]]

שאלה מבחינה על שימוש בזריקת חריגות יורשות מ-Exception
![[Pasted image 20240715011422.png]]

> [!important] משהו חמוד שיש בדוגמה פה זה העניין של מחלקה גנרית שאז לא צריך את הסוגריים המשולשות בפונקציה כדי להצהיר על פרמטר

# תפיסת חריגות
![[Pasted image 20240715013121.png]]

![[Pasted image 20240715013143.png]]

יכול להיות שזו שאלה מוכרת במבחנים?!
![[Pasted image 20240715013153.png]]

## Checked vs Unchecked Exceptions
יש Checked Exceptions שהם Exceptionים שיודעים בזמן קימפול שהקוד מודע לכך שפונקציה מסויימת לדוגמה זורקת את ה-Exception הידוע הזה, ולכן הקוד שלנו (הפונקציה שלנו) תצטרך להצהיר שהיא עלולה לזרוק את סוג ה-Exception הספציפי (אם לא נעשה זאת נקבל שגיאת קומפילציה)
יש גם עניין של Partial Checked (שבהיררכית הירושה של ה-Exception יש גם Unchecked וגםChecked Exceptions)

דוגמה ל-Checked
![[Pasted image 20240716220333.png]]
