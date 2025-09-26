import React from 'react';
import { Link } from '@inertiajs/react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useForm } from '@inertiajs/react';


interface FormData {
    status: string,
    executor: string,
    labels: string,
    self_tasks: string
}
export default function Index( props ) {
    const tasks = props.tasks;
    const statuses = props.statuses
    const users = props.users
    const labels = props.labels
    const filter = props.filter
    const { data, setData, get, processing, errors } = useForm<FormData>({
        status: filter.status,
        executor: filter.executor,
        labels: filter.labels,
        self_tasks: filter.self_tasks,
    })
    
    const formData = new FormData();
    formData.append('status', data.status);
    formData.append('executor', data.executor);
    formData.append('labels', data.labels);
    formData.append('self_tasks', data.self_tasks);
    
      const handleSubmit  = (e: React.FormEvent) => {
        e.preventDefault()
        get('/tasks/', {
          data: formData,
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      }
  return (
    
      <div>
        <Header />
        <main>
            <div class="container-md mt-3">
                <h1>Tasks</h1>
                <Link href="/tasks/create/" class="btn btn-primary">Create task</Link>
                <div class="container-md bg-body-tertiary mt-3 mb-3 border rounded-3">
                    <div class="p-3">
                        <form className="form-inline center" onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label className="form-label" htmlFor="id_status">Статус</label>
                                <select name="status" className="form-select ml-2 mr-3" id="id_status" value={data.status} onChange={(e) => setData('status', e.target.value)}>
                                    <option value="" >---------</option>
                                    {statuses && statuses.map(status => (
                                        <option value={status.id}>{status.name}</option>
                                    ))}</select><br />
                            </div>
                            <div className="mb-3">
                                <label className="form-label" htmlFor="id_executor">Исполнитель</label>
                                <select name="executor" className="form-select mr-3 ml-2" id="id_executor" value={data.executor} onChange={(e) => setData('executor', e.target.value)}>
                                    <option value="" selected="">---------</option>
                                    {users && users.map(user => (
                                        <option value={user.id} selected="">{user.first_name} {user.last_name}</option>
                                    ))}</select><br />
                            </div>
                            <div className="mb-3">
                                <label className="form-label" htmlFor="id_label">Метка</label>
                                <select name="label" className="form-select mr-3 ml-2" id="id_label" value={data.labels} onChange={(e) => setData('labels', e.target.value)}>
                                    <option value="" selected="">---------</option>
                                    {labels && labels.map(label => (
                                    <option value={label.id} selected="">{label.name}</option>
                                    ))}</select><br />
                            </div>
                            <div className="mb-3">
                                <div className="form-check">
                                    <input type="checkbox" name="self_tasks" className="form-check-input mr-3" id="id_self_tasks" checked={data.self_tasks} onChange={(e) => setData('self_tasks', e.target.checked)}/>
                                    <label className="form-check-label" htmlFor="id_self_tasks">Только свои задачи</label>
                                </div>
                            </div>
                            <input className="btn btn-primary" type="submit" value="Показать" />
                        </form>
                    </div>
                </div>
                <table class="table table-striped mt-2" data-test="checks">
                    <thead>
                        <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Status</th>
                        <th>Autor</th>
                        <th>Executor</th>
                        <th>Create date</th>
                        <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {tasks && tasks.map(task => (
                        <tr>
                            <td>{ task.id }</td>
                            <td><Link href={`/tasks/${task.id}/`}>{ task.name }</Link></td>
                            <td>{ task.status }</td>
                            <td>{ task.author }</td>
                            <td>{ task.executor }</td>
                            <td>{ task.created_at}</td>
                            <td>
                                <Link href={`/tasks/${task.id}/update/`}>Edit</Link><br />
                                <Link href={`/tasks/${task.id}/delete/`}>Delete</Link>
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



