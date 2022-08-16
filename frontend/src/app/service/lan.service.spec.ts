import { TestBed, inject } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { LanService } from './lan.service';

describe('LanService', () => {
  let httpTestingController: HttpTestingController;
  let lanService: LanService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });

    httpTestingController = TestBed.get(HttpTestingController);
  });

  beforeEach(inject([LanService], (service: LanService) => {
    lanService = service;
  }));
});
