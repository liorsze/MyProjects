package util

import (
	"testing"

	"github.com/stretchr/testify/require"
	"golang.org/x/crypto/bcrypt"
)

func TestPassword(t *testing.T)  {
	password := RandomString(6)

	hashedPassword1, err := HashPassword(password)
	require.NoError(t,err)
	require.NotEmpty(t,hashedPassword1)

	err = CheckPassword(password,hashedPassword1)
	require.NoError(t,err)

	// check wrong password
	wrongPassword := RandomString(6)
	err = CheckPassword(wrongPassword,hashedPassword1)
	require.EqualError(t,err,bcrypt.ErrMismatchedHashAndPassword.Error())

	// differnt value for the same password
	hashedPassword2, err := HashPassword(password)
	require.NoError(t,err)
	require.NotEmpty(t,hashedPassword2)
	require.NotEqual(t,hashedPassword1,hashedPassword2)
}