# Python-UMA-Implementation
Takes templated input data via csv and creates customized output files based on client specified parameters and requirements.

- csv files are the test source data files. They are loaded in to the data frames and transacted on. They should not be edited.
- ClientTemplate.py is the superclass. It loads the data from the source files in to a dataframe and prepares the data frame to be transacted on by the individual client objects, which are the subclass of ClientTemplate.py.
- Clients.py: subclass of ClientTemplate. Takes the standard client template and customizes it based on the client and/or client template. Some things that are customized by client/template are cash symbol, weight column name, cash restrictions.
- DFHelpers: helper functions to update fields in the provided data frame. Returns the updated data frame.
- Email: template function to auto create emails.
- ProRata: current state is not integrated; however, will be a function to prorate cash for a client based on their minimum cash weight. For example, if current cash is 1% and the client cannot accept a file with cash less than 2%, ProRata.py will prorate 1% of cash out of securities based on their weights to proportionately raise the 1% cash required to submit the file.
- Main.py: Loops through the cleint_dict and client_email dictoinaries to create all the files based on client parameters.
