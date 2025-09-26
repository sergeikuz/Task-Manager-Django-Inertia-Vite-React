import React from 'react';
import { Link } from '@inertiajs/react';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Index( props ) {
    const statuses = props.statuses;
  return (
    
      <div>
        <Header />
        <main>
            <div class="container-md mt-3">
                <h1>Statuses</h1>
                <Link href="/statuses/create/" class="btn btn-primary">Create status</Link>
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
                        {statuses && statuses.map(status => (
                        <tr>
                            <td>{ status.id }</td>
                            <td>{ status.name }</td>
                            <td>{ status.created_at }</td>
                            <td>
                                <Link href={`/statuses/${status.id}/update/`}>Edit</Link><br />
                                <Link href={`/statuses/${status.id}/delete/`}>Delete</Link>
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
