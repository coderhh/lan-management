import { TestBed, inject } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { AccountService } from './account.service';

describe('AccountService', () => {
  let httpTestingController: HttpTestingController;
  let accountService: AccountService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    httpTestingController = TestBed.get(HttpTestingController);
  });
  beforeEach(inject([AccountService], (service: AccountService) => {
    accountService = service;
  }));
});
