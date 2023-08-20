# احراز کاربران در کنار دیوار

در این پروژه یک کلاینت oauth برای احراز افراد از طریق دیوار پیاده سازی شده است.
پروتکل استفاده شده برای احراز در دیوار ، از پروتکل oauth2 پیروی میکند و با استفاده از فریم ورک جنگو پیاده سازی شده است. در ادامه جزئیات استفاده از این کلاینت را شرح میدهیم:
اپلیکیشنی را در نظر بگیرید که نیاز به گذاشتن افزونه روی یک آگهی داشته باشد. برای تحقق این امر ، نیاز به توکن آگهی و اجازه ی کاربر برای مورد ذکر شده است. به این منظور نیاز است کاربر از اپلیکیشن مبدا به اپلیکیشن دیوار منتقل شود و اجازه های مورد نیاز را به اپلیکیشن بدهد.
این url شامل اطلاعات زیر است:
- یک state که یک رشته ی تصادفی است که اپلیکیشن برای هر ریکوئست درخواست ایجاد میکند.
- یک scope شامل لیستی از دسترسی هایی که نیاز است. هر پرمیشن با فرمت `$PERMISSION_TYPE__$RESOURCE_ID` آورده میشود.
  - مقدار permission_type میتواند برابر با USER_PHONE باشد ، این پرمیشن نیازی به resource_id ندارد و یا میتواند برابر با ADDON_USER_APPROVED باشد که نیازمند توکن آگهی به عنوان resource_id است.
- یک آدرس redirect_url که نشان دهنده ی این است که بعد از تایید دسترسی ها توسط کاربر ، اطلاعات `authentication_code` به چه اندپوینتی ارسال شود.

در فایل `handler/views.py` یک اندپوینت به نام oauth_login وجود دارد که در ریکوئست نیاز به وارد کردن resource_id است ، در مثال بالا ، ریسورس مورد نیاز ، توکن آگهی است. با دادن این اطلاعات ، کاربر به یک url از دیوار منتقل میشود. در صورتی که کاربر در دیوار لاگین باشد و توکن آگهی متعلق به شماره ی لاگین شده باشد ، فرد میتواند جزئیات دسترسی های درخواست شده را مشاهده کند ، اکشن های مجاز برای کاربر ، "تایید" و "رد" است ، در صورتی که کاربر اجازه ی دسترسی ها را تایید کند ، oauth_callback (همان redirect url) با ورودی های code و state فراخوانی خواهد شد. code بیانگر authentication_code ای است که سرور برای مجموعه پرمیشن های تایید شده ی کاربر تولید کرده است و state نیز باید برابر با همان state ای باشد که اپلیکیشن در ریکوئست خود قرار داده بود.
پس از دریافت authentication_code ، باید key exchange صورت بگیرد. برای این منظور یک ریکوئست دیگر به اندپوینت 
```http request
https://api.divar.ir/v1/open-platform/oauth/access_token
```
ارسال میکنیم و در آن علاوه بر authentication_code ، سکرت اپلیکیشن را نیز در آن قرار میدهیم. در این جا سکرت برای عملیات exchange همان api-key است که توسط دیوار جنریت شده و به شرکت ها داده شده است.
با ارسال این ریکوئست ، اگر کمتر از ۳ روز از ساخت authentication_code گذشته باشد ، اندپوینت مربوطه توکن access_token را در ریسپانس قرار میدهد. نیاز است این توکن ، به علاوه ی پرمیشن ها و توکن آگهی و ... در دیتابیس ذخیره شود تا در ریکوئست های آینده از آن استفاده شود.  

برای نمونه ما در انتهای اندپوینت oauth_callback یک ریکوئست به اندپوینت 
```http request
https://api.divar.ir/v1/open-platform/users
```
ارسال کرده ایم و شماره ی فرد را دریافت میکنیم.
