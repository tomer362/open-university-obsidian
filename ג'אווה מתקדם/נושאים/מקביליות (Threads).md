# יצירת תהליכון (Thread)
יש 3 אפשרויות ליצירת תהליכון
![[Pasted image 20240715014229.png]]

דוגמה לאפשרות 1
![[Pasted image 20240715014509.png]]

דוגמה לאפשרות 2 (זה נחמד כשאנחנו כבר יורשים ממחלקה אחרת נניח)
![[Pasted image 20240715014534.png]]

דוגמה לאפשרות 3
![[Pasted image 20240715014601.png]]


## שימוש ב-join
חשוב לשים לב להשתמש ב-try catch על ה-join כי הוא עלול להקפיץ  InterruptedException, אותו דבר עם Thread.sleep
![[Pasted image 20240715014820.png]]

## מניעה הדדית
איך לפתור מניעה הדדית
![[Pasted image 20240715014940.png]]

### synchronized static
סתם אנקדוטה על שיטות שהן synchornized static, אם יש ל-class שמוגן ע"י synchornized משתנים סטטיים ורוצים לגעת בהם אז צריך לעשות את זה מפונקציה שהיא מוגדרת כ-synchornized static
והמקור של זה:
![[Pasted image 20240716195135.png]]
