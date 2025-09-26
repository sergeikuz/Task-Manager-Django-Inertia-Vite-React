import React from 'react';
import { Link } from '@inertiajs/react';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Index( props ) {
    const users = props.users;
    const error = props.error;
  return (
    
      <div>
        <Header />
        <main>
            <div class="container-md mt-3">
                {error && (
                    <div className="alert alert-danger alert-dismissible fade show">
                        {error}
                    </div>
                )}
                <h1>Users</h1>
                <table class="table table-striped mt-2" data-test="checks">
                    <thead>
                        <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Full name</th>
                        <th>Create date</th>
                        <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {users && users.map(user => (
                            <tr>
                                <td>{ user.id }</td>
                                <td>{ user.username }</td>
                                <td>{ user.first_name } { user.last_name }</td>
                                <td>{ user.date_joined }</td>
                                <td>
                                    <Link href={`/users/${user.id}/update/`}>Edit</Link><br />
                                    <Link href={`/users/${user.id}/delete/`}>Delete</Link>
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
