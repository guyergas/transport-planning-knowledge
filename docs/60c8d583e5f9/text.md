=== PAGE 1 === [text-layer]
vol4meta.xlsx




                                                                                                                                                                                        Authorמשרד התחבורה
                                                                                                                                                                                        Publisherמשרד התחבורה
                                                                                                                                                                                             Contactדנה מורנוב
                                                                                                                                                                               gis_support@pgl.co.il Contact Email
                                                                                                                                                   Titleמאגר ספירות תנועה תלתן  -כרך ( 4 ספירות אחרי )2020
                                    Descriptionקובץ זה מרכז את המידע שנצבר במאגר ספירות תנועה ארצי. מאגר זה הוא מאגר שיתופי ביוזמת משרד התחבורה, שאוסף ספירות תנועה שבוצעו באופן מזדמן בצמתים ובקטעים.
              המאגר כולל ספירות שבוצעו לצורכי פרויקטים, בדיקות תחבורתיות, עדכון רמזורים וכיו"ב, ואינו כולל ספירות של מערכות ניטור המשכיות כגון ספירות של מערכות בקרת תנועה ו"-סל הספירות הלאומי".
         ספירות התנועה הינם ספירות של כלי רכב בכביש, ומתחלקות בין ספירות צומת, הסופרות את הרכבים לפי כווני התנועה בצומת, וספירות חתך, שסופרות כלי רכב החוצים חתך מסויים בדרך לפי כוון הנסיעה.
                                                                                                                     הספירות מתקבלות במאגר ע"פ הפורמט האחוד של ספירות תנועה של משרד התחבורה.
                                                                                                  הספירות מונגשות באופן אינטראקטיבי באמצעות מערכות מידע תלתן ומערכת מידע חצב של משרד התחבורה.
                                                                                                                                                                                          22/03/2022 Created
                                                                                                                                                                                                   1.4 Version
                                                                                                                                                                                          05/05/2026 Last updated
                                                                                                                                                                     Temporal coverageכל הספירות במאגר אחרי שנת 2020
                                                                                                                                                                                tiltancounts-vol4.zip Dataset file
                                                                                                                                                                                          05/05/2026 Metadata creation date
                                         Commentsהמידע על ספירות התנועה מאורגנת באמצעות שתי טבלאות. הטבלה הראשונה כוללת רשימת ספירות עם קוד מזהה ומידע על הספירה, והשנייה היא טבלת נפחי התנועה .
                                                                    ספירות התנועה מוגדרות ע"פ כללי הפורמט האחוד לספירות תנועה של משרד התחבורה ומוגדרות גיאוגרפית ע"פ קואורדינטה וזרועות הספירה.
                                                                                              ע"פ כללי פורמט אחוד זרועות הספירות ממוספרות עם כוון השעון החל מזרוע הספירה הראשון ברביע הצפון-מזרחי.
                                                                                                                            הנפחים מוגדרים בין זרועות הספירה (מזרוע לזרוע) לפי תקופת בצבירה וסוג רכב.
                                                                                        סוגי הרכב הינם בהתאם לסוג המקורי שנספר בספירה כפי שהוגדר ע"י מזמין הספירה, בהתאם למילון כלי הרכב המצורף.
                                                                                                                                                                      הקבצים מקודדים באמצעות utf-8
                                                                                          Related documentsפורמט אחוד ספירות תנועה ()https://www.gov.il/he/departments/policies/uniform_format_traffic_counts
                                                                                                                                                       מערכת תלתלן ()/https://tiltan.ayalonhw.co.il
                                                                                                                                                         מילון סוגי רכב ( קובץ  vehicletypes.csvמצורף)
                                                                                                                                                                  Keywordsספירות תנועה,סווג כלי רכב,נפחי תנועה
                                                                                                                                                                           Frequency of updateמאגר זה יתעדכן אחת לרבעון.
                                                                                                                                                                                                   Spatial coverageארצי
                                                                                                                          Creative Commons Attribution http://opendefinition.org/licenses/cc-by License
                                               Data qualityספירות התנועה שמתקבלות במאגר אושרו על ידי גוף המזמין של הספירה. אין המאגר מבצע בדיקה של איכות הנתונים ומגיש אותם כפי שבוצעו על ידי מזמין הספירה.
                                                                                                                                                                                                       URL
                                                                                                                                                                                       vol4counts.csv Files list
                                                                                                                                                                                         vol4data.csv




1 of 2

=== PAGE 2 === [text-layer; table]
vol4meta.xlsx


                                                                                                                                     Files
                                                                                                                      vol4counts.csv File name
                                                                                                                                 CSV File format
                                                                                                   File descriptionרשימת ספירות התנועה הכלולות בקובץ
                                                                                                                     Israel_TM_Grid Spatial reference system
                                                                                   [143072.04, 383557.19] - [170165.83, 638450.96] Geographic bounding
         label                value       comment                            description                 type                  name File Fields
                                      קוד חד ערכי, מקשר לטבלת הנפחים                   מזהה ספירה      number                countid
                              צומת                                        האם זו ספירת צומת או קטע      string                  type
                              קטע
                                                                                 תיאור מקום הספירה       string                 desc
                                                    פורמט dd/mm/yy                   תאריך הספירה         date                  date
                                                         פורמט h:mm                   שעת התחלה           time                 start
                                                         פורמט h:mm                      שעת סיום         time                   end
                 כל רבע שעה    15            משך הזמן שנצברו הנתונים                        תקופה       number                period
                    כל שעה     60
                                                                                   שם מזמין הספירה       string                 client
                                                                             שם חברת ביצוע הספירה        string              executor
                                                                               קו רוחב מקום הספירה      number                       x
                                                                               קו אורך מקום הספירה      number                       y
                                                                                       מספר זרועות      number                   arms
                                                                                          שם זרוע 1      string                    st1
                                                                                         זווית זרוע 1   number                     az1
                                                                                          שם זרוע 2      string                    st2
                                                                                         זווית זרוע 2   number                     az2
                                                                                          שם זרוע 3      string                    st3
                                                                                         זווית זרוע 3   number                     az3
                                                                                          שם זרוע 4      string                    st4
                                                                                         זווית זרוע 4   number                     az4
                                                                                          שם זרוע 5      string                    st5
                                                                                         זווית זרוע 5   number                     az5
                                                                                          שם זרוע 6      string                    st6
                                                                                         זווית זרוע 6   number                     az6
                                           הערות מיוחדות במידה ונשרמו                 הערות לספירה       string            comments
                                                                                                                         vol4data.csv File name
                                                                                                                                  CSV File format
                                                                                                             File descriptionקובץ נפחים בספירות התנועה
                                                   File Commentsכל רשומה בקובץ כוללת נפח תנועה לפי כוון נסיעה, תקופה וסוג רכב בהתאמה להגדרות הספירה
         label                value       comment                            description                  type                  name File Fields
                                                                                       מזהה ספירה       number      countid
                                      ספציפי לצומת ע"פ טבלת הספירות                 קוד לזרוע כניסה     number      fr
                                      ספציפי לצומת ע"פ טבלת הספירות                 קוד לזרוע יציאה     number      to
                                                     ע"פ מילון סוגי רכב                    סוג רכב       string     vehtype
                                                         פורמט h:mm                  תחילת תקופה          time      periodstrt
                                                                                     מספר כלי רכב       number      volume


2 of 2
