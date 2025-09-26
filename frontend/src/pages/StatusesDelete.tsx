import React from 'react';
import { Link } from '@inertiajs/react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useForm } from '@inertiajs/react';


export default function Index(props) {
    const status = props.status;
    const { data, setData, post, processing, errors } = useForm()

    const handleSubmit  = (e: React.FormEvent) => {
    e.preventDefault()
    post(`/statuses/${status.id}/delete/`, {
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
            <div className="container">
                <div className="row justify-content-center mt-3">
                    <h1 className="display-5">Deleting status</h1>
                    <p className="lead">Are you sure you want to delete { status.name }?</p>
                    <form onSubmit={handleSubmit}>
                        <button type="submit">Delete</button>
                    </form>  
                </div>
            </div>
            </main>
        <Footer />
      </div>
  );
}
