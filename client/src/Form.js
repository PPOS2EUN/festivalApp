import React from "react";
import { useForm } from "react-hook-form";
import styled from "styled-components";
import './Form.css';

const Styles = styled.div`
  padding: 20px;
  background: lavender;
  height: 1225px;
  
 h1 {
   border-bottom: 1px solid white;
   color: #3d3d3d;
   font-family: sans-serif;
   font-size: 20px;
   font-weight: 600;
   line-height: 24px;
   padding: 10px;
   text-align: center;
 }

 form {
   background: white;
   border: 2px solid #dedede;
   display: flex;
   flex-direction: column;
   justify-content: space-around;
   margin: 0 auto;
   padding: 30px 50px;
   height: 60%;
 }

 input, button{
   border: 1px solid #d9d9d9;
   border-radius: 4px;
   box-sizing: border-box;
   padding: 10px;
   width: 100%;
 }

 label {
   color: #3d3d3d;
   display: block;
   font-family: sans-serif;
   font-size: 35px;
   font-weight: 300;
 }

 .error {
   color: red;
   font-family: sans-serif;
   font-size: 12px;
   height: 30px;
 }

 .submitButton {
   background-color: #6976d9;
   color: white;
   font-family: sans-serif;
   font-size: 35px;
   font-weight: 300;
   margin: 20px 0px;
`;

export default function Form() {
    const onLinkClick = (e) => {

    };
    const { register, handleSubmit } = useForm();
    let today = new Date();

    let hours = today.getHours();
    let minutes = today.getMinutes();

    let year = today.getFullYear();
    let month = today.getMonth() + 1;
    let date = today.getDate();

     return (
       <Styles>
           <h3 style={{textAlign: 'center', fontSize: '40px'}}>Visitor Form</h3>
           <form>
               <label>Name</label>
               <input name="name"/>

               <label>Age</label>
               <input name="name"/>

               <label>Phone number</label>
               <input name="pnum"/>

               <label>Email</label>
               <input name="email"/>

               <button onClick={} type="submit" className="submitButton">Submit</button>
           </form>
       </Styles>
     );
}
