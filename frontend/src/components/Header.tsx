import React from "react";
import {Link} from '@inertiajs/react';
import { If, Then, Else, Fallback } from 'react-if';
import { usePage } from '@inertiajs/react';

function Header() {
    const { props } = usePage();
    const { auth } = props;

    return (
        <header>
            <nav className="navbar navbar-expand-lg bg-body-tertiary">
                <div className="container-fluid">
                    <Link className="navbar-brand" href="/">Task manager</Link>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        
                        <ul className="navbar-nav me-auto d-flex align-items-center" style={{ flexWrap: 'nowrap' }}>
                            <li className="nav-item">
                                <Link className="nav-link" href="/users/">Users</Link>
                            </li>
                            {auth?.isAuthenticated && (
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" href="/statuses/">Statuses</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" href="/labels/">Labels</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" href="/tasks/">Tasks</Link>
                                    </li>
                                </>
                            )}
                        </ul>
                        
                        <ul className="navbar-nav ms-auto d-flex align-items-center" style={{ flexWrap: 'nowrap' }}>
                            {auth?.isAuthenticated ? (
                                <li className="nav-item">
                                    <Link 
                                        href="/logout/" 
                                        method="post" 
                                        as="button" 
                                        className="btn btn-outline-primary ms-2"
                                    >
                                        Exit
                                    </Link>
                                </li>
                            ) : (
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" href="/login/">Login</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" href="/users/create/">Registration</Link>
                                    </li>
                                </>
                            )}
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
}

export default Header;