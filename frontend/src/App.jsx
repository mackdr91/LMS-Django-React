import { Route, Routes, BrowserRouter } from "react-router-dom";
import MainWrapper from "./layouts/MainWrapper";
import PrivateRoute from "./layouts/PrivateRoute";

import Register from "./views/auth/Register";
import Login from "./views/auth/Login";

function App() {
  return (

    <BrowserRouter> {/* Router */}
      <MainWrapper> {/* MainWrapper */}
        <Routes> {/* Routes */}
          <Route path="/register/" element={<Register />} /> {/* Register page */}
          <Route path="/login/" element={<Login />} /> {/* Login page */}
        </Routes>
      </MainWrapper>
    </BrowserRouter>
  );
}

export default App;
