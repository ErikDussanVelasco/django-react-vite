import { BrowserRouter, Routes, Route,Navigate } from "react-router-dom";
import {Page1} from "./pages/Page1";  // Importación correcta
import {Pageform} from  "./pages/Pageform";
import {Navigation} from './components/Navegation';


function App() {
  return (
    <BrowserRouter>
      <Navigation/>


      <Routes>
        <Route path="/" element={<Navigate to ="/tasks"/>} />  // cambio de pagina automatico 
        <Route path="/tasks" element={<Page1 />} /> 
        <Route path="/tasks-create" element={<Pageform />} /> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;
