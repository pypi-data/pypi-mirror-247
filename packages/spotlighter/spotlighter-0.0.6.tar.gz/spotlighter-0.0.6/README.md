# SPOTLIGHT

## Ver

v0.0.6 DD 231218

## 목적

Spotlight upload를 위한 정형화된 전처리 자동화

## 주요기능

1. 전처리

* Excel to Text  
* concatenate text  
* check text header (TEST)    
* Merge Text (i.e. BSEG+BKPF) (if already set df, automatically transferred to dfA)    

2. DF to SQL(IMPORT)

* To Insert to SQL, Read columns'length  
* Create Table => with mySQL  
* Import file and Insert to DB  

3. MAIN RUN 

* Read text to dataframe  
* Auto_MAP : MAP_GL.xlsx 파일을 활용하여 columns 자동 매핑 + 추가  
* Modify mode(After Auto_MAP)  
* To recon G/L and T/B, export SUM(AMT LC)groupby Acct  

3-1. MODIFY MOD

3-1-1. 전처리-전표금액

* replace string (Kill comma, space, regex etc.)  
* Apply DC (차변은 +, 대변은 - 처리)  
* To Minus () or - : 문자열 () 또는 후위-인 경우 마이너스로 변환  
* Multiple 100  : 곱하기 100  
* FROM 전표금액 TO 차대금액  : signed 전표금액에서 unsigned 차변/대변을 생성한다.  
* FILLNA(0)  : N/A를 0으로 채운다.  
* 자동수동 : 특정 컬럼값(전표성격, 사용자 등)이 특정 문자열(복수 가능)을 포함하는 행을 A로 지정  

3-1-2. 전처리-기타

* drop a column  
* drop duplicate  
* Change column name  
* Change column datatype  
 
4. SAVE TO..

* Save text  
* Save a part of df(특정 계정과목 추출 등)  

5. 일반기능

* MANUAL HANDLING - DEBUG  
* df.info()  
* df.head(10)  

## Help
FA&A 박형원