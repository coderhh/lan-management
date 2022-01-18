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

const accountsKey = 'lan-accounts';
const accountsKeyStr = localStorage.getItem(accountsKey);
let accounts: any[] = [];
if (accountsKeyStr !== null){
  accounts = JSON.parse(accountsKeyStr);
} else {
  accounts.push({email: 'yehanghan@gmail.com', password:'12345678', isVerified: true, refreshTokens: []});
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
          // case url.endsWith('/accounts/revoke-token') && method === 'POST':
          //     return revokeToken();
          // case url.endsWith('/accounts/register') && method === 'POST':
          //     return register();
          // case url.endsWith('/accounts/verify-email') && method === 'POST':
          //     return verifyEmail();
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

    function getRefreshToken(): string {
      // get refresh token from cookie
      return (document.cookie.split(';').find(x => x.includes('fakeRefreshToken')) || '=').split('=')[1];
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

    function generateJwtToken(account: { id: any; }) {
      // create token that expires in 15 minutes
      const tokenPayload = {
          exp: Math.round(new Date(Date.now() * 15 * 60 * 1000).getTime() / 1000),
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
  }
}

export let fakeBackendProvider = {
  provide: HTTP_INTERCEPTORS,
  useClass: FakeBackendInterceptor,
  multi: true
};



