from flask import Flask,render_template,request,url_for
from collections import defaultdict
app=Flask(__name__)

class user:
    def __init__(self,name,):
        self.name=name
        

@app.route("/home")
def homepage():
    return render_template("home.html")

@app.route("/calculate",methods=["POST"])
def trip_amount_split():
    name=list(request.form.getlist('name'))
    amount=list(request.form.getlist('amount'))
    amt={}
    for n,a in zip(name,amount):
        amt[n]=int(a)
    # total=0
    # for am in amt.values():
    #     total+=am
    # total/=len(amount)
    # for x in amt.keys():
    #     amt[x]-=total
    # return amt

    def simplify_amounts(amounts):
        simplified_amounts = []

        positive_amounts = {person: amount for person, amount in amounts.items() if amount > 0}
        negative_amounts = {person: -amount for person, amount in amounts.items() if amount < 0}

        while positive_amounts and negative_amounts:
            creditor = max(positive_amounts, key=positive_amounts.get)
            debtor = max(negative_amounts, key=negative_amounts.get)

            credit_amount = positive_amounts[creditor]
            debit_amount = negative_amounts[debtor]

            if credit_amount > debit_amount:
                simplified_amounts.append((debtor, creditor, debit_amount))
                positive_amounts[creditor] -= debit_amount
                del negative_amounts[debtor]
            elif credit_amount < debit_amount:
                simplified_amounts.append((debtor, creditor, credit_amount))
                positive_amounts[creditor] = 0
                negative_amounts[debtor] -= credit_amount
            else:
                simplified_amounts.append((debtor, creditor, debit_amount))
                del positive_amounts[creditor]
                del negative_amounts[debtor]

        return simplified_amounts
    
    total_spent = sum(amt.values())

    average_spent = total_spent / len(amt)

    amounts = {person: amount - average_spent for person, amount in amt.items()}

    transactions = simplify_amounts(amounts)

    return render_template("result.html",trns=transactions)
    
@app.route("/details",methods=['POST'])
def details():
    n=int(request.form.get('n'))
    rt_name=request.form.get('rt_name')
    return render_template("calculator.html",n=n,rt_name=rt_name)



if __name__=="__main__":
    app.run(debug=True)