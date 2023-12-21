# <img src="https://www.spartaquant.com/assets/img/spartaquant/icon-color.png" width="60px" alt="SpartaQuant icon" class="logo-default"> SpartaQuant

This API provides many services you can use from Spartacloud


##### Installation

Install the package via pip with code below:

```python
pip install spartacloud
```

To Upgrade:


```python
pip install --upgrade spartacloud
```

##### Authentication

1. First, you must create an account at https://spartaquant.pro/login
2. Retrieve your API token in the profile section
3. Click on Copy access key (to clipboard the access key)
4. Import the spartaquant module
```python
import spartaquant as sq
sq = sq.spartaquant()
```
5. Enter the access key in the prompt box
6. You are logged !


##### Examples	

Some examples to start with the SpartaQuant API:

1. Retrieve the list of available SpartaQuant objects
```python
import spartaquant as sq
sq = sq.spartaquant()
sq.getDataDB()
```

2. Retrieve the list of available SpartaQuant functions
```python
import spartaquant as sq
sq = sq.spartaquant()
sq.getFunctionDB()
```

3. Get a specific object by apiId (find apiId with sq.getDataDB())
```python
import spartaquant as sq
sq = sq.spartaquant()
sq.getData(apiId)
```

4. Run a SpartaQuant function by apiId (find apiId with sq.runFunction())
```python
import spartaquant as sq
sq = sq.spartaquant()
sq.runFunction(apiId, *args)
```

5. Store data into SpartaQuant
```python
import spartaquant as sq
sq = sq.spartaquant()
sq.putData(dataObj, name=None, apiId=None, dateDispo=None)
```

6. Retrieve the list of available XLS SpartaQuant files
```python
import spartaquant as sq
sq = sq.spartaquant()
sq.getXlsDB()
```

7. Create an XLS file in SpartaQuant

```python
import spartaquant as sq
sq = sq.spartaquant()
sq.createXls(nameFile, extension='xlsx')
```
8. Update and XLS file in SpartaQuant

```python
import spartaquant as sq
sq = sq.spartaquant()
sq.putXlsData(xlsId, data_df, sheetName, cellStart='A1', clearSheet=True)
```


Check out the documentation of the API at https://spartaquant.pro/publicAPI for more information