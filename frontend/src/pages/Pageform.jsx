import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { createTask, deleteTask, updateTask ,getTask} from "../api/Tienda.api";// añade tareas a la pagina(post)
import { useNavigate, useParams  } from 'react-router-dom' //redirecciona de la pagina de los registro a donde quedan registrados
//use params extrae los parametros que tengo en la url
import {toast} from 'react-hot-toast' //visual
export function Pageform() {
    const {
        register,
        handleSubmit,
        setValue,
        formState: { errors },
    } = useForm();

    const navigate = useNavigate();
    const params = useParams();
    console.log(params) //si hay un valor params estoy editando


    //update(actualizar)

    const onSubmit = handleSubmit(async (data) => {
        if (params.id) {
            await updateTask(params.id , data);
            console.log("actualizando");
            toast.success('Producto actualizado ', {
                position: "bottom-right",
                style: {
                    background :"#101010",
                    color: "#fff"
                }
            //crear producto(create)
            })
        } else {
            await createTask(data)
            console.log("creando nuevo producto");
            toast.success('Producto creado ', {
                position: "bottom-right",
                style: {
                    background :"#101010",
                    color: "#fff"
                }
            
            })
            
        }

        navigate("/tasks");
    });

    useEffect(()  => {
        async function loadTask() {
            if (params.id){
                const res = await getTask(params.id);
                
                setValue('codigo', res.data.codigo)
                setValue('nombre', res.data.nombre)
                setValue('descripcion', res.data.descripcion)
                setValue('precio_compra', res.data.precio_compra)
                setValue('precio_venta', res.data.precio_venta)
                setValue('stock', res.data.stock)
            }
        }
        loadTask();
        
    }, []);

    //debo eliminar descripcion y acomodarlo en los models
    return (
        <div>
            <form onSubmit={onSubmit}>
                <input
                    type="number"
                    placeholder="Código"
                    {...register("codigo", { required: true })}
                />
                {errors.codigo && <span>El código es obligatorio</span>}

                <input
                    type="text"
                    placeholder="Nombre"
                    {...register("nombre", { required: true })}
                />
                {errors.nombre && <span>El nombre es obligatorio</span>}
                <textarea
                    rows="3"
                    placeholder="Descripción"
                    {...register("descripcion")}
                ></textarea>

                <input
                    type="number"
                    step="0.001"
                    placeholder="Precio de compra"
                    {...register("precio_compra", { required: true })}
                />
                {errors.precio_compra && <span>El precio de compra es obligatorio</span>}

                <input
                    type="number"
                    step="0.001"
                    placeholder="Precio de venta"
                    {...register("precio_venta", { required: true })}
                />
                {errors.precio_venta && <span>El precio de venta es obligatorio</span>}

                <input
                    type="number"
                    placeholder="Stock"
                    {...register("stock", { required: true })}
                />
                {errors.stock && <span>El stock es obligatorio</span>}

                <button>Guardar</button>
            </form>


            {params.id && <button onClick={async () => {
                const accepted = window.confirm('¿Estas seguro?')
                if (accepted) {
                    await deleteTask(params.id);
                    console.log("Producto eliminado");
                    toast.success('Producto eliminado ', {
                        position: "bottom-right",
                        style: {
                            background :"#101010",
                            color: "#fff"
                        }
            
                    })
                    navigate("/tasks");

                }
            }}>Borrar</button>}

        </div>
    );
    
}
//si params.id existe mostrar el boton borrar
