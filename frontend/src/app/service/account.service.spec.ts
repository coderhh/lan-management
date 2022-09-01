import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Account } from '../models/account';
import { AccountService } from './account.service';
import { environment } from '../../environments/environment';

const baseUrl = `${environment.apiUrl}/account/`;

describe('AccountService', () => {
  let service: AccountService;
  let httpMock: HttpTestingController;
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, RouterTestingModule],
      providers: [AccountService]
    });
    service = TestBed.inject(AccountService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('be able to retrieve accounts from API bia GET', () => {
    const dummyAccounts: Account[] = [
      {
        public_id: '1',
        last_name: 'last_name'
      },
      {
        public_id: '2',
        last_name: 'last_name'
      }
    ];
    service.getAll().subscribe((accounts) => {
      expect(accounts.length).toBe(2);
      expect(accounts).toEqual(dummyAccounts);
    });
    const request = httpMock.expectOne(baseUrl);
    expect(request.request.method).toBe('GET');
    request.flush(dummyAccounts);
  });

  it('be able to create account from API bis POST', () => {
    const dummyAccount = {
      public_id: '1',
      last_name: 'last_name'
    };

    service.create(dummyAccount).subscribe((account) => {
      expect(account).toEqual(dummyAccount);
    });
    const request = httpMock.expectOne(baseUrl);
    expect(request.request.method).toBe('POST');
  });

  afterEach(() => {
    httpMock.verify();
  });
});
