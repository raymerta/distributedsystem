# DISTRIBUTED SYSTEM : SIMPLE WEB SERVER FOR COLLABORATIVE EDITING

To run the web server : 
- run this : python server.py 

# SHARING STRATEGY : HANDLED BY SERVER

Server stores all the documents, the clients do create new documents or modify
existing.
	- Clients cannot edit the document off-line
	- All the concurrency and editing conflicts are resolved by server
	- Server maintains the ownership/permissions:

		//to be filled
		- what document is allowed to be edited by which clients,
		- who is the owner of what document.


Asynchronous or lock-free strategies (using document versions)
	- Version control is required

# REQUIREMENTS : 

Nonetheless, you implementation has to meet some requirements and they are as follows:
1. Real-time. The collaborative editor should be capable of providing the real-time response due to editing and viewing the changes.
2. Tenacity. User should be able to edit a document over several sessions:
	a) user should be able to continue editing from where he left the document
	b) in case there were changes introduced by other users the document must reflect them once a users is editing the document again
3. Multiple users. The collaborative editor should allow at least three users to work simultaneously.
4. Textual format. Allowing ASCII text and handling the line breaks.

