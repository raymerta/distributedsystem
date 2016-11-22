
var message = 'Hello World!';var myAjax = new Ajax.Request(
            'index', // relative uri to server 
            {
                method: 'get',
                parameters: 'message=' + encodeURIComponent(message)
                onComplete: alertResponse
            }
);
 
function alertResponse(reply)
{
    // just print the JSON notation response in an alert message
    alert('JSON: ' + reply.responseText);
}
