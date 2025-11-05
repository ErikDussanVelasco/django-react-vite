import {useEffect} from 'react'
import {getAllTasks} from '../api/Tienda.api'


export function List() {
useEffect(() => {    //apenas arracnque la pagina quiero que muestre

//console.log('pagina loaded') nos sirve para mostrar en la consola de la web
    async function loadTasks(){
        const res = await getAllTasks ();// recivo la respuesta y la guardo
        console.log(res);
    }
    loadTasks();
},[]);
    
    
    
    
    return(
        <div> List</div>
    )
}