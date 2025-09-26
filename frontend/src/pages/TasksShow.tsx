import React from 'react';
import { Link } from '@inertiajs/react';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Show( props ) {
    const task = props.task;
  return (
    
      <div>
        <Header />
        <main>
            <div className="container-md mt-3">
                <h1>View task</h1>
                <div className="container bg-secondary text-white border rounded-3 rounded-bottom-0 py-2 px-3">
                    <h2>{ task.name }</h2>
                </div>
                <div className="container bg-light border rounded-3 rounded-top-0 p-3">
                    <p>{ task.description }</p>
                    <hr />
                    <div className="container ">
                        <div className="row p-1">
                            <div className="col">Author</div>
                            <div className="col">{ task.author }</div>
                        </div>
                        <div className="row p-1">
                            <div className="col">Executor</div>
                            <div className="col">{ task.executor }</div>
                        </div>
                        <div className="row p-1">
                            <div className="col">Status</div>
                            <div className="col">{ task.status }</div>
                        </div>
                        <div className="row p-1">
                            <div className="col">Date of creation</div>
                            <div className="col">{ task.created_at }</div>
                        </div>
                        <div className="row p-1">
                            <div className="col">
                            <h6>Labels:</h6>
                            <ul>
                                {task.labels && task.labels.map(label => (
                                    <li>{ label.name }</li>
                                ))}              
                            </ul>
                            </div>
                        </div>
                        <div className="row p-1">
                            <div className="col">
                            <Link href={`/tasks/${task.id}/update/`}>Edit</Link><br />
                            <Link href={`/tasks/${task.id}/delete/`}>Delete</Link>
                            </div>
                        </div>
                    </div>
                </div>
                </div>
            </main> 
        <Footer />
      </div>
  );
}
