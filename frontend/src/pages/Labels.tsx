import React from 'react';
import { Link } from '@inertiajs/react';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Index( props ) {
    const labels = props.labels;
  return (
    
      <div>
        <Header />
        <main>
            <div class="container-md mt-3">
                <h1>Labels</h1>
                <Link href="/labels/create/" class="btn btn-primary">Create labels</Link>
                <table class="table table-striped mt-2" data-test="checks">
                    <thead>
                        <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Create date</th>
                        <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {labels && labels.map(label => (
                        <tr>
                            <td>{ label.id }</td>
                            <td>{ label.name }</td>
                            <td>{ label.created_at }</td>
                            <td>
                                <Link href={`/labels/${label.id}/update/`}>Edit</Link><br />
                                <Link href={`/labels/${label.id}/delete/`}>Delete</Link>
                            </td>
                        </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            </main>
        <Footer />
      </div>
  );
}
