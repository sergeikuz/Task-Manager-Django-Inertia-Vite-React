import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useForm } from '@inertiajs/react';

interface FormData {
    name: string,
}

console.log('Form data before submit:')
export default function Create(props) {
    const error = props.error
  const { data, setData, post, processing, errors } = useForm<FormData>({
    name: '',
  })

  const formData = new FormData();
    formData.append('name', data.name);

  const handleSubmit  = (e: React.FormEvent) => {
    e.preventDefault()
    post('/labels/create/', {
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
    <h1>Labels</h1>
    {error && (
        <ul className="list-unstyled text-danger">
            <li>{error}</li></ul>
        )}
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label className="form-label" htmlFor="name">Name:</label>
        <input className="form-control" id="name" name="name" value={data.name} onChange={(e) => setData('name', e.target.value)} /><br />
      </div>
      <button className="btn btn-primary" type="submit">Create</button>
    </form>
    </div>
    </main>
        <Footer />
    </div>
  )
}
