import React from 'react'
import BaseHeader from '../partials/BaseHeader'
import BaseFooter from '../partials/BaseFooter'
import { Link, useNavigate } from 'react-router-dom'

import { useEffect, useState } from 'react'
import apiInstance from '../../utils/axios'
import { register } from '../../utils/auth'


function Register() {

  const [full_name, setFullName] = useState("") // set the full_name state
  const [email, setEmail] = useState("") // set the email state
  const [password, setPassword] = useState("") // set the password state
  const [password2, setPassword2] = useState("")  // set the password2 state
  const [isLoading, setIsLoading] = useState(false) // set the loading state

  const Navigate = useNavigate()

/*
e.target.value  is a reference to the element that triggered the event.
 In this case, it's the input element with the id "full_name".
The value of this element is the full name entered by the user.
*/

/**
 * Handles the form submission for user registration.
 * Prevents the default form submission behavior, sets the loading state,
 * and attempts to register the user with the provided full name, email,
 * and passwords. If registration is successful, navigates to the home
 * page and displays a success message. If there is an error, alerts the user
 * with the error message.
 *
 * @param {Event} event - The form submission event.
 */
  const handleSubmit = async (event) => {

    event.preventDefault(); // prevent the form from submitting
    setIsLoading(true); // set the loading state to true

    const {error} = await register(full_name, email, password, password2) // register the user
    if (error) { // if there is an error
      alert(error); // alert the user
      setIsLoading(false)
    } else{
      Navigate('/')
      alert("Registration successful! You have been logged in.")
      setIsLoading(false)
    };
  };




  return (
    <>
      <BaseHeader />

      <section className="container d-flex flex-column vh-100" style={{ marginTop: "150px" }}>
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Sign up</h1>
                  <span>
                    Already have an account?
                    <Link to="/login/" className="ms-1">
                      Sign In
                    </Link>
                  </span>
                </div>
                {/* Form */}
                <form className="needs-validation" noValidate="" onSubmit={handleSubmit}>
                  {/* Username */}
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Full Name</label>
                    <input
                      type="text"
                      id="full_name"
                      className="form-control"
                      name="full_name"
                      placeholder="John Doe"
                      required=""
                      onChange={(e) => setFullName(e.target.value)}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email Address</label>
                    <input
                      type="email"
                      id="email"
                      className="form-control"
                      name="email"
                      placeholder="johndoe@gmail.com"
                      required=""
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>

                  {/* Password */}
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">Confirm Password</label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e) => setPassword2(e.target.value)}
                    />
                  </div>
                  <div>
                    <div className="d-grid">
                      { isLoading === true && (
                         <button disabled type="submit" className="btn btn-primary">
                         Processing <i className='fas fa-spinner fa-spin'></i>
                       </button>

                      ) }

                      { isLoading === false && (
                         <button type="submit" className="btn btn-primary">
                         Sign Up <i className='fas fa-user-plus'></i>
                       </button>
                      ) }

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
  )
}

export default Register