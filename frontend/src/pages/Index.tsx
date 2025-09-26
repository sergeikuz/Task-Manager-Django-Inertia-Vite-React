import React from 'react';
import { Link } from '@inertiajs/react';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Index() {

  return (
    
      <div>
        <Header />
        <main>
          <div className="container">
            <div className="row justify-content-center mt-3">
              <div className="col-12 bg-light border rounded-3 p-5">
                <h1 className="display-3">Greetings from Hexlet!</h1>
                <p className="lead">Practical programming courses</p>
                <div>
                    <a href="https://ru.hexlet.io" className="btn btn-primary">Learn more</a>
                </div>        
              </div>
            </div>
          </div>
        </main>
        <Footer />
      </div>
  );
}
