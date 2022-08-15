import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { Account } from '../models/account';
import { environment } from '../../environments/environment';
import { finalize, map } from 'rxjs/operators';

const baseUrl = `${environment.apiUrl}/account`;
const authUrl = `${environment.apiUrl}/auth`;
@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private accountSubject: BehaviorSubject<Account>;
  public account: Observable<Account>;
  private initialAccount: Account = new Account();
  constructor(private http: HttpClient, private router: Router) {
    this.accountSubject = new BehaviorSubject<Account>(this.initialAccount);
    this.account = this.accountSubject.asObservable();
  }

  public get accountValue(): Account {
    return this.accountSubject.value;
  }

  login(email: string, password: string): Observable<Account> {
    return this.http
      .post<Account>(
        `${authUrl}/login`,
        { email, password },
        { withCredentials: true }
      )
      .pipe(
        map((account) => {
          this.accountSubject.next(account);
          this.startRefreshTokenTimer();
          return account;
        })
      );
  }

  logout(): void {
    this.http
      .post<Account>(`${authUrl}/logout`, {}, { withCredentials: true })
      .subscribe();
    this.stopRefreshTokenTimer();
    this.accountSubject.next(this.initialAccount);
    this.router.navigate(['/home']);
  }

  getAll(): Observable<Account[]> {
    return this.http.get<Account[]>(`${baseUrl}/`);
  }

  getById(id: string): Observable<Account> {
    return this.http.get<Account>(`${baseUrl}/${id}`);
  }

  create(params: object): Observable<Account> {
    return this.http.post<Account>(`${baseUrl}/`, params);
  }

  update(id: string, params: object): Observable<Account> {
    return this.http.put<Account>(`${baseUrl}/${id}`, params).pipe(
      map((account: Account) => {
        if (account.public_id === this.accountValue.public_id) {
          account = { ...this.accountValue, ...account };
          this.accountSubject.next(account);
        }
        return account;
      })
    );
  }

  delete(id: string) {
    return this.http.delete(`${baseUrl}/${id}`).pipe(
      finalize(() => {
        if (id === this.accountValue.public_id) this.logout();
      })
    );
  }

  refreshToken(): Observable<Account> {
    return this.http
      .post<Account>(`${authUrl}/refresh-token`, {}, { withCredentials: true })
      .pipe(
        map((account) => {
          // console.log(account)
          this.accountSubject.next(account);
          this.startRefreshTokenTimer();
          return account;
        })
      );
  }

  private refreshTokenTimeout!: NodeJS.Timeout;
  stopRefreshTokenTimer() {
    clearTimeout(this.refreshTokenTimeout);
  }
  private startRefreshTokenTimer() {
    // parse json object from base64 encoded jwt token
    const jwtTokenEncoded = this.accountValue?.jwtToken;
    if (jwtTokenEncoded) {
      const jwtToken = JSON.parse(atob(jwtTokenEncoded.split('.')[1]));
      // set a timeout to refresh the token a minute before it expires
      const expires = new Date(jwtToken.exp * 1000);
      const timeout = expires.getTime() - Date.now() - 60 * 1000;
      this.refreshTokenTimeout = setTimeout(
        () => this.refreshToken().subscribe(),
        timeout
      );
    }
  }
}
