SQLCommand command = new SqlCommand("SELECT customerid as ID,Firstname + '' + lastname as Name,companyname as Company, emailaddressas Email,phone FROM saleslt.customer WHERE EmailAddress = @0", cnn);
command.Parameters.Add(new SqlParameter("0", 1));

