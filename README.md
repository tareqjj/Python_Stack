# Python_Stack



# An overall description of the software:

The software allows the user to register into the platform and process transactions (buy/sell) based on the user's choice of currency. The user must register with a debit card to process payment and receive funds after exchange. Exchange rates are handled by a third party API and updated hourly. An admin account manages users access and privileges and has a dashboard of current site activity/load.

the home page contains historical exchange rates data displayed in a carousel as charts 

![image](https://user-images.githubusercontent.com/66148148/110348933-d8e0c600-803a-11eb-87b4-901b90eeb754.png)

in order to access the service you need to rigester 

![image](https://user-images.githubusercontent.com/66148148/110351264-4f7ec300-803d-11eb-803c-5d955c5700af.png)

when you register the aplication redirects you to your news feed page where you can see you transactions history and a column chart of the current rates 

![image](https://user-images.githubusercontent.com/66148148/110351442-80f78e80-803d-11eb-9034-b16fc7858adc.png)

and the form in the top is the form to order a new transaction where you enter the currency you want to change from and the desired currency in exchange and the ammount then it is gonna ask you to enter your payment info.
Note that this is aplicable with debit card only and you have to have a bank account of the desired currency.

![image](https://user-images.githubusercontent.com/66148148/110351761-d59b0980-803d-11eb-851d-e85ee345b526.png)

here we need to connect the aplication with a third party to actually excute the transfer but until this point we are registering the  transaction and it appears on the user's new feed
