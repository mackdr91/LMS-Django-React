import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";
import { useState, useEffect } from "react";
import apiInstance from "../../utils/axios";
import { useNavigate, useSearchParams } from "react-router-dom";

function CreateNewPassword() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParam] = useSearchParams();

  const otp = searchParam.get("otp");
  const uuidb64 = searchParam.get("uuid");
  const refresh_token = searchParam.get("refresh_token");

/**
 * Handles the submission of the new password form.
 * Prevents the default form behavior and sets the loading state.
 * If the passwords do not match, an alert is shown and the process is halted.
 * Otherwise, it creates a FormData object with the OTP, UUID, password, and refresh token,
 * and sends a POST request to the password change endpoint.
 * On success, navigates the user to the login page and alerts the success message.
 * On error, logs the error and alerts the error message.
 *
 * @param {Event} e - The form submission event.
 */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    if (confirmPassword !== password) {
      alert("Passwords do not match");
      return;
    } else {
      const formData = new FormData();
      formData.append("otp", otp); // data for class PasswordChangeAPIView in api/views.py
      formData.append("uuidb64", uuidb64); // data for class PasswordChangeAPIView in api/views.py
      formData.append("password", password);// data for class PasswordChangeAPIView in api/views.py
      formData.append("refresh_token", refresh_token);// data for class PasswordChangeAPIView in api/views.py

      try {
        await apiInstance
          .post("user/password-change/", formData) // send a POST request to the password change endpoint
          .then((res) => {
            console.log(res.data);
            alert(res.data.message);
            setIsLoading(false);
            navigate("/login/");
          });
      } catch (err) {
        console.log(err);
        alert(err.response.data.message);
        setIsLoading(false);
      }
    }
  };

  return (
    <>
      <BaseHeader />

      <section
        className="container d-flex flex-column vh-100"
        style={{ marginTop: "150px" }}
      >
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Create New Password</h1>
                  <span>Choose a new password for your account</span>
                </div>
                <form
                  className="needs-validation"
                  noValidate=""
                  onSubmit={handleSubmit}
                >
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Enter New Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e) => setPassword(e.target.value)}
                    />
                    <div className="invalid-feedback">
                      Please enter valid password.
                    </div>
                  </div>

                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                    <div className="invalid-feedback">
                      Please enter valid password.
                    </div>
                  </div>

                  <div>
                    <div className="d-grid">
                      {isLoading === true && (
                        <button
                          disabled
                          type="submit"
                          className="btn btn-primary"
                        >
                          Processing <i className="fas fa-spinner fa-spin"></i>
                        </button>
                      )}

                      {isLoading === false && (
                        <button type="submit" className="btn btn-primary">
                          Save New Password{" "}
                          <i className="fas fa-check-circle"></i>
                        </button>
                      )}
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  );
}

export default CreateNewPassword;
