import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useForm } from '@inertiajs/react';

interface FormData {
    name: string,
    description: string,
    status: string,
    author: string,
    executor: string,
    labels: string
}

console.log('Form data before submit:')
export default function Update(props) {
    const error = props.error
    const task = props.task
    const statuses = props.statuses
    const users = props.users
    const labels = props.labels
  const { data, setData, post, processing, errors } = useForm<FormData>({
    name: task.name,
    description: task.description,
    status: task.status,
    author: task.author,
    executor: task.executor,
    labels: task.labels,
  })

  const formData = new FormData();
    formData.append('name', data.name);

  const handleSubmit  = (e: React.FormEvent) => {
    e.preventDefault()
    post('/tasks/create/', {
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
    <div className="container-md mt-3">
    <h1>Task</h1>
    {error && (
        <ul class="errorlist">
            <li>{error}</li></ul>
        )}
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label className="form-label" htmlFor="name">Name:</label>
        <input className="form-control" id="name" name="name" value={data.name} onChange={(e) => setData('name', e.target.value)} /><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="description">Description:</label>
        <input className="form-control" id="description" name="description" value={data.description} onChange={(e) => setData('description', e.target.value)} /><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="name">Status:</label>
        <select className="form-select" id="status" name="status" value={data.status} onChange={(e) => setData('status', e.target.value)}>
          <option value="" selected="">---------</option>
        {statuses && statuses.map(status => (
          <option value={`${status.id}`} selected="">{status.name}</option>
        ))}</select><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="author">Author:</label>
        <select className="form-select" id="author" name="author" value={data.author} onChange={(e) => setData('author', e.target.value)}>
          <option value="" selected="">---------</option>
        {users && users.map(user => (
          <option value={`${user.id}`} selected="">{user.first_name} {user.last_name}</option>
        ))}</select><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="executor">Executor:</label>
        <select className="form-select" id="executor" name="executor" value={data.executor} onChange={(e) => setData('executor', e.target.value)}>
          <option value="" selected="">---------</option>
        {users && users.map(user => (
          <option value={`${user.id}`} selected="">{user.first_name} {user.last_name}</option>
        ))}</select><br />
      </div>
      <div className="mb-3">
        <label className="form-label" htmlFor="name">Labels:</label>
        <select className="form-select" id="labels" name="labels" value={data.labels} onChange={(e) => setData('labels', e.target.value)}>
          <option value="" selected="">---------</option>
        {labels && labels.map(label => (
          <option value={`${label.id}`} selected="">{label.name}</option>
        ))}</select><br />
      </div>
      <button className="btn btn-primary" type="submit">Create</button>
    </form>
    </div>
    </main>
        <Footer />
    </div>
  )
}
