import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useForm } from '@inertiajs/react';

interface FormData {
    first_name: string,
    last_name: string,
    username: string,
    password1: string,
    password2: string
}

console.log('Form data before submit:')
export default function Update( props ) {
  const user = props.user
  const error = props.error
  const { data, setData, post, processing, errors } = useForm<FormData>({
    first_name: user.first_name,
    last_name: user.last_name,
    username: user.username,
    password1: user.password,
    password2: user.password,
  })
  

  const formData = new FormData();
    formData.append('first_name', data.first_name);
    formData.append('last_name', data.last_name);
    formData.append('username', data.username);
    formData.append('password', data.password1);

  const handleSubmit  = (e: React.FormEvent) => {
    e.preventDefault()
    post(`/users/${user.id}/update/`, {
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onError: (errors) => {
        console.error('Form submission errors:', errors);
      },
    });
  }

  return (
    <div>
        <Header />
        <main>
    <div className="container-md mt-3">
    <h1>Update User</h1>
    {error && (
        <ul className="list-unstyled text-danger">
            <li>{error}</li></ul>
        )}
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label className="form-label" htmlFor="first_name">First name:</label>
        <input className="form-control" type="text" id="first_name" name="first_name" value={data.first_name} onChange={(e) => setData('first_name', e.target.value)} /><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="last_name">Last name:</label>
        <input className="form-control" type="text" id="last_name" name="last_name" value={data.last_name} onChange={(e) => setData('last_name', e.target.value)} /><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="username">Username:</label>
        <input className="form-control" type="text" id="username" name="username" value={data.username} onChange={(e) => setData('username', e.target.value)}/><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="password1">Password:</label>
        <input className="form-control" id="password1" name="password1" value={data.password1} type="password" onChange={(e) => setData('password1', e.target.value)}/><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="password2">Password:</label>
        <input className="form-control" id="password2" name="password2" value={data.password2} type="password" onChange={(e) => setData('password2', e.target.value)}/><br />
      </div>
      <button className="btn btn-primary" type="submit">Отправить</button>      
    </form>
    </div>
    </main>
        <Footer />
    </div>
  )
}
