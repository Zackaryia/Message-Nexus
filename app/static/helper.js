const request = async ( url, params = {}, method = 'GET' ) => {
    let options = {
        method
    };
    if ( 'GET' === method ) {
        
    } else {
        options.body = JSON.stringify( params );
    }
    
	const response = await fetch( url, options ).then( response => response.json() );
    return response
};

const get_request = ( url, params ) => request( url, params, 'GET' );
const post = ( url, params ) => request( url, params, 'POST' );