string connectionString;
System.Data.SqlClient.SqlConnection cnn;
connectionString = @"Data Source=xxx.database.windows.net;Initial Catalog=xxx;User ID=xxx ;Password=xxx ";
cnn = new SqlConnection(connectionString);
SqlCommand command = new SqlCommand ("SELECT customerid as ID,Firstname + ' ' + lastname as Name,companyname as Company, emailaddress as Email,phone FROM saleslt.customer WHERE EmailAddress = '" + txtEmail.Text + "'", cnn);
