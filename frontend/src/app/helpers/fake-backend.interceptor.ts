import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpResponse,
  HTTP_INTERCEPTORS
} from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { AlertService } from '../service/alert.service';
import { delay, dematerialize, materialize } from 'rxjs/operators';
import { Role } from '../models/role';

const accountsKey = 'lan-accounts';
const accountsKeyStr = localStorage.getItem(accountsKey);
let accounts: any[] = [];
if (accountsKeyStr !== null){
  accounts = JSON.parse(accountsKeyStr);
} else {
  accounts.push({id: 1, firstName:'yehang', lastName:'han', Role:'Admin', email: 'yehanghan@gmail.com', password:'12345678', isVerified: true, refreshTokens: []});
}

@Injectable()
export class FakeBackendInterceptor implements HttpInterceptor {

  constructor(private alertService: AlertService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const { url, method, headers, body} = request;
    const alertService = this.alertService;

    return handleRoute();

    function handleRoute() {
      switch (true){
          case url.endsWith('/authenticate') && method === 'POST':
            return authenticate();
          case url.endsWith('/refresh-token') && method === 'POST':
            return refreshToken();
          case url.endsWith('/revoke-token') && method === 'POST':
            return revokeToken();
          case url.endsWith('/accounts') && method === 'GET':
            return getAccounts();
          case url.match(/\/accounts\/\d+$/) && method === 'GET':
            return getAccountById();
          case url.endsWith('/accounts') && method === 'POST':
            return createAccount();
          case url.match(/\/accounts\/\d+$/) && method === 'PUT':
            return updateAccount();
          case url.match(/\/accounts\/\d+$/) && method === 'DELETE':
            return deleteAccount();
          default:
              return next.handle(request);
      }
    }

    function authenticate() {
      const { email, password } = body;
      const account = accounts.find(x => x.email === email && x.password === password && x.isVerified);

      if (!account) { return error('Email or Password is incorrect.'); }

      // add refresh token to account
      account.refreshTokens.push(generateRefreshToken());
      localStorage.setItem(accountsKey, JSON.stringify(accounts));

      return ok({
          ...basicDetails(account),
          jwtToken: generateJwtToken(account)
      });
    }

    function refreshToken() {
      const refreshToken  = getRefreshToken();

      if (!refreshToken) return unauthorized();

      const account = accounts.find(x => x.refreshTokens.includes(refreshToken));

      if (!account) return unauthorized();

      // replace old refresh token with a new one and save
      account.refreshTokens = account.refreshTokens.filter((x: string) => x !== refreshToken);
      account.refreshTokens.push(generateRefreshToken());
      localStorage.setItem(accountsKey, JSON.stringify(accounts));

      return ok({
          ...basicDetails(account),
          jwtToken: generateJwtToken(account)
      });
    }

    function revokeToken(){
      if(!isAuthenticated()) return unauthorized();

      const refreshToken = getRefreshToken();
      const account = accounts.find(x => x.refreshTokens.includes(refreshToken));

      //revoke token and save
      account.refreshTokens = account.refreshTokens.filter((x: string) => x !== refreshToken);
      localStorage.setItem(accountsKey, JSON.stringify(accounts));
      return ok();
    }
    function getAccounts(){
      if (!isAuthenticated()) return unauthorized();
      return ok(accounts.map(x => basicDetails(x)));
    }

    function getAccountById(){
      if (!isAuthenticated()) return unauthorized();

      let account = accounts.find(x => x.id === idFromUrl());

      if (account.id !== currentAccount().id && !isAuthorized(Role.Admin)) {
        return unauthorized();
      }

      return ok(basicDetails(account));

    }

    function createAccount(){
      if (!isAuthorized(Role.Admin)) return unauthorized();
      const account = body;
      if (accounts.find(x => x.email === account.email)){
        return error(`Email ${account.email} is already registered`);
      }

      account.id = newAccountId();
      account.dateCreated = new Date().toISOString();
      account.isVerified = true;
      account.refreshTokens = [];
      delete account.confirmPassword;
      accounts.push(account);
      localStorage.setItem(accountsKey, JSON.stringify(accounts));

      return ok();
    }

    function updateAccount(){
      if(!isAuthenticated()) return unauthorized();

      let params = body;
      let account = accounts.find(x => x.id === idFromUrl());

      if(account.id !== currentAccount().id && !isAuthorized(Role.Admin)) {
        return unauthorized();
      }
      // only update password if included
      if(!params.password)
      {
        delete params.password;
      }
      // don't save confirm password
      delete params.confirmPassword;

      // update and save account
      Object.assign(account, params);
      localStorage.setItem(accountsKey, JSON.stringify(accounts));

      return ok(basicDetails(account));
    }
    function deleteAccount(){
      if(!isAuthenticated()) return unauthorized();
      let account = accounts.find(x => x.id === idFromUrl());

      if (account.id !== currentAccount().id && !isAuthorized(Role.Admin))
      {
        return unauthorized();
      }

      // delete account then save
      accounts = accounts.filter(x => x.id !== idFromUrl());
      localStorage.setItem(accountsKey, JSON.stringify(accounts));

      return ok();
    }
    function getRefreshToken(): string {
      // get refresh token from cookie
      return (document.cookie.split(';').find(x => x.includes('fakeRefreshToken')) || '=').split('=')[1];
    }
    function isAuthenticated() {
      return !!currentAccount();
    }
    function isAuthorized(role: Role)
    {
      const account = currentAccount();
      if(!account) return false;
      return account.role === role;
    }
    function newAccountId(): number {
      return accounts.length ? Math.max(...accounts.map(x => x.id)) + 1 : 1;
    }
    function currentAccount(): any {
      // check if jwt token is in auth header
      const authHeader = headers.get('Authorization');
      if (!authHeader?.startsWith('Bear fake-jwt-token')) return;

      // check if token is expired
      const jwtToken = JSON.parse(atob(authHeader.split('.')[1]));
      const tokenExpired = Date.now() > (jwtToken.exp * 1000);
      if (tokenExpired) return;

      const account = accounts.find(x => x.id === jwtToken.id);
      return account;
  }

    function error(message: string) {
      return throwError({ error: { message }})
          .pipe(materialize(), delay(500), dematerialize());
    }

    function generateRefreshToken(): string {
      const token = new Date().getTime().toString();

      // add token cookie that expires in 7 days
      const expires = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toUTCString();
      document.cookie = `fakeRefreshToken=${token}; expires=${expires}; path=/`;

      return token;
    }

    function generateJwtToken(account: { id: number; }) {
      // create token that expires in 15 minutes
      const tokenPayload = {
          exp: Math.round(new Date(Date.now() + 15 * 60 * 1000).getTime() / 1000),
          id: account.id
      };
      return `fake-jwt-token.${btoa(JSON.stringify(tokenPayload))}`;
    }

    function basicDetails(account: any): { id: any; title: any; firstName: any; lastName: any; email: any; role: any; dateCreated: any; isVerified: any; } {
      const { id, title, firstName, lastName, email, role, dateCreated, isVerified } = account;
      return { id, title, firstName, lastName, email, role, dateCreated, isVerified };
    }

    function ok(body?: any) {
      return of(new HttpResponse( { status: 200, body}))
          .pipe(delay(500));
    }


    function unauthorized(): Observable<any> {
       return throwError({status: 401, error: { message: 'Unauthorized'}})
              .pipe(materialize(), delay(500), dematerialize());
    }

    function idFromUrl()
    {
      const urlParts = url.split('/');
      return parseInt(urlParts[urlParts.length - 1]);
    }
  }
}

export let fakeBackendProvider = {
  provide: HTTP_INTERCEPTORS,
  useClass: FakeBackendInterceptor,
  multi: true
};



