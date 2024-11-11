import { Route, Routes, BrowserRouter } from "react-router-dom";
import MainWrapper from "./layouts/MainWrapper";
import PrivateRoute from "./layouts/PrivateRoute";

import Register from "./views/auth/Register";
import Login from "./views/auth/Login";
import Logout from "./views/auth/Logout";
import ForgotPassword from "./views/auth/ForgotPassword";

function App() {
  return (

    <BrowserRouter> {/* Router */}
      <MainWrapper> {/* MainWrapper */}
        <Routes> {/* Routes */}
          <Route path="/register/" element={<Register />} /> {/* Register page */}
          <Route path="/login/" element={<Login />} /> {/* Login page */}
          <Route path="/logout/" element={<Logout />} /> {/* Logout page */}
          <Route path="/forgot-password/" element={<ForgotPassword />} /> {/* ForgotPassword page */}
        </Routes>
      </MainWrapper>
    </BrowserRouter>
  );
}

export default App;
