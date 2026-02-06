Requirements for Front End:
Node
Angular CLI
Ngx Toastr
Bootstrap 5.3.3 CDN


Run the Frontend Application
ng serve
http://localhost:4200/automate 

Run the Backend Application
python -m flask run
http://127.0.0.1:5000/


Sample Request for

Validate File
http://127.0.0.1:5000/validate
{
    "id":"1770375431583-87697",
    "file_name":"taxi_010E33SD547.pdf"
}

Response

{
    "is_valid": true
}

Process File

http://127.0.0.1:5000/process

Response

{
    "message": "Success"
}

Get Receipts 
http://127.0.0.1:5000/receipts

Response
[
    {
        "created_at": "2026-02-06T16:27:15.090952",
        "file_path": "C:\\Users\\Varun Maddi\\Desktop\\Automate_Accounts_Project\\Automate_Accounts\\uploads\\taxi_010E33SD547.pdf",
        "id": "1770375431583-87697",
        "merchant_name": "รร",
        "purchased_at": "2026-02-06T16:27:15.081372",
        "total_amount": 14.54,
        "updated_at": "2026-02-06T16:27:15.090952"
    },
    {
        "created_at": "2026-02-06T18:34:03.988376",
        "file_path": "C:\\Users\\Varun Maddi\\Desktop\\Automate_Accounts_Project\\Automate_Accounts\\uploads\\applebees_8267120140431.pdf",
        "id": "1770383041524-55831",
        "merchant_name": "BAR؛؛ NÉIŨHBr]RHr)i.)ỨGÍ'íĩlL",
        "purchased_at": "2026-02-06T18:34:03.988376",
        "total_amount": 7.49,
        "updated_at": "2026-02-06T18:34:03.988376"
    }
]

Get Receipts by ID
http://127.0.0.1:5000/receipts/1770383041524-55831

{
    "created_at": "2026-02-06T18:34:03.988376",
    "file_path": "C:\\Users\\Varun Maddi\\Desktop\\Automate_Accounts_Project\\Automate_Accounts\\uploads\\applebees_8267120140431.pdf",
    "id": "1770383041524-55831",
    "merchant_name": "BAR؛؛ NÉIŨHBr]RHr)i.)ỨGÍ'íĩlL",
    "purchased_at": "2026-02-06T18:34:03.988376",
    "total_amount": 7.49,
    "updated_at": "2026-02-06T18:34:03.988376"
}




