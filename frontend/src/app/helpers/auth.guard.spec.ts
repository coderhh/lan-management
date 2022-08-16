import { AuthGuard } from './auth.guard';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('AuthGuard', () => {
  beforeEach(() =>
    TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      providers: [AuthGuard]
    })
  );

  it('should be created', () => {
    const interceptor: AuthGuard = TestBed.inject(AuthGuard);
    expect(interceptor).toBeTruthy();
  });
});
