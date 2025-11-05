export const getAllTasks = () => { // cuando se ejecute la funcion digo que ejecute axios
    return axios.get('http://127.0.0.1:8000/api/Productos/') 
//peticion del backend de donde pedimos  informacion

}