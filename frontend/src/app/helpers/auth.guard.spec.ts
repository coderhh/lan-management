import { AuthGuard } from './auth.guard';
import { TestBed } from '@angular/core/testing';

describe('AuthGuard', () => {
  beforeEach(() =>
    TestBed.configureTestingModule({
      providers: [AuthGuard]
    })
  );

  it('should be created', () => {
    const interceptor: AuthGuard = TestBed.inject(AuthGuard);
    expect(interceptor).toBeTruthy();
  });
});
